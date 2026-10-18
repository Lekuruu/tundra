
from collections.abc import Callable

from twisted.internet.interfaces import IListeningPort
from twisted.internet.protocol import Factory
from twisted.internet import reactor

from .world import GameObject, Position, World
from .protocol import MetaplaceProtocol
from .places import PlacePresentation
from .serialization import Command
from .session import SessionState

import logging

TokenDecoder = Callable[[str], dict | None]

EMPTY_TILEMAP = (
    'iVBORw0KGgoAAAANSUhEUgAAAEAAAAAoCAAAAABrpaM1AAAANElEQVRIiWNgGAWjYBSMghEJ'
    'GEEAhzAc4BDGqoSgykFrALo55BoAN2XUgFEDiM+Jo2BQAwDdDQLtiDfyPgAAAABJRU5ErkJggg=='
)
EMPTY_HEIGHTMAP = (
    'iVBORw0KGgoAAAANSUhEUgAAAEEAAAApCAAAAABPOxuuAAAAIklEQVRIie3MIQEAAAACIKc7'
    '3RFWGED6isFgMBgMBoPBcBgfzjTMSGY6zQAAAABJRU5ErkJggg=='
)

# taking reference from:
# https://web.archive.org/web/20170201071457/http://protocol.clubpenguinwiki.info/wiki/Mobile_API
# lets see what works and what doesn't ...

class BasicCommandHandler:
    """Implements the smallest mobile metaplace login and place handshake."""

    def __init__(
        self,
        world: World,
        token_decoder: TokenDecoder,
        presentation: PlacePresentation | None = None,
        base_asset_url: str = ' ',
    ) -> None:
        self.world = world
        self.token_decoder = token_decoder
        self.presentation = presentation or PlacePresentation()
        self.base_asset_url = base_asset_url
        self.logger = logging.getLogger(f'{world.name}.commands')

    def __call__(self, protocol: MetaplaceProtocol, command: Command) -> None:
        handlers = {
            '/user_agent': self.handle_user_agent,
            '/version': self.handle_version,
            '/login': self.handle_login,
            '/ready': self.handle_ready,
            '/place_ready': self.handle_place_ready,
        }
        handler = handlers.get(command.name)

        if handler is None:
            self.logger.debug('Unsupported command %s', command.name)
            return

        handler(protocol, command)

    def handle_user_agent(self, protocol: MetaplaceProtocol, command: Command) -> None:
        user_agent = ' '.join(str(argument) for argument in command.arguments)
        protocol.user_agent = user_agent
        protocol.send_tag('S_USERAGENT', 0, user_agent)

    def handle_version(self, protocol: MetaplaceProtocol, command: Command) -> None:
        protocol.send_tag('S_VERSION', 'FY15-20150206 (4954)r')

    def handle_login(self, protocol: MetaplaceProtocol, command: Command) -> None:
        protocol.send_tag('S_LOGINDEBUG', 'Got /login command from user')

        if protocol.session.state is not SessionState.CONNECTED:
            self.reject_login(protocol)
            return

        if len(command.arguments) != 3:
            self.reject_login(protocol)
            return

        if not all(isinstance(argument, str) for argument in command.arguments):
            self.reject_login(protocol)
            return

        # make the linter shut up already please
        arguments: list[str] = command.arguments # type: ignore

        server_type, player_id_input, token = arguments

        if not player_id_input.isdigit():
            self.reject_login(protocol)
            return

        player_id = int(player_id_input)
        token_data = self.token_decoder(token)

        if token_data is None:
            self.reject_login(protocol)
            return

        if (token_player_id := token_data.get('id')) is None:
            self.reject_login(protocol)
            return

        if server_type.lower() != 'live' or token_player_id != player_id:
            self.reject_login(protocol)
            return

        protocol.player_name = str(token_data.get('name', ''))
        protocol.session.authenticate(player_id)
        protocol.send_tag('S_LOGINDEBUG', 'Successfully verified credentials server-side')
        protocol.send_tag('S_LOGINDEBUG', 'Finalizing login, creating final user object')
        protocol.session.enter_world()
        protocol.send_tag('W_BASEASSETURL', self.base_asset_url)
        protocol.send_tag('W_DISPLAYSTATE')
        protocol.send_tag('W_ASSETSCOMPLETE', player_id)

    def handle_ready(self, protocol: MetaplaceProtocol, command: Command) -> None:
        if protocol.session.state is not SessionState.IN_WORLD:
            return

        place = self.world.start_place

        if place is None:
            self.logger.error('No start place defined for world %s', self.world.name)
            protocol.close_connection()
            return

        protocol.send_tag(
            'W_INPUT', 'use', '0:10', 2, 3, 0, 'use'
        )
        protocol.send_tag(
            'W_INPUT', 'touch-the-terrain', '0:8600033', 1, 6, 0, 'path_terrain'
        )
        protocol.send_tag(
            'W_INPUT', 'mouse-the-terrain', '0:8600033', 1, 3, 0, 'path_terrain'
        )
        protocol.session.enter_place(place.place_id)
        self.send_place(protocol)
        self.logger.debug('Sent place data to player %s', protocol.session.player_id)

    def handle_place_ready(self, protocol: MetaplaceProtocol, command: Command) -> None:
        if protocol.session.state is not SessionState.PLACE_READY or protocol.place_ready:
            return

        if (player_id := protocol.session.player_id) is None:
            return

        if protocol.session.place is None:
            self.logger.error('Player %s is not in a place', protocol.session.player_id)
            protocol.close_connection()
            return

        camera = self.presentation.camera
        protocol.send_tag('P_CAMERA', *camera.position, 0, 1)
        protocol.send_tag('P_ZOOM', camera.zoom)
        protocol.send_tag('P_LOCKZOOM', camera.lock_zoom)
        protocol.send_tag('P_LOCKCAMERA', camera.lock_camera)

        player = GameObject(
            player_id,
            protocol.player_name,
            '0:2480001',
            '0:1',
            Position(*self.presentation.start_position),
        )
        protocol.session.show_object(player)
        self.send_avatar_data(protocol, player_id)
        protocol.send_tag('O_PLAYER', player_id)
        protocol.place_ready = True
        self.logger.debug(
            'Player %s is now ready in place %s',
            player_id,
            protocol.session.place.place.place_id,
        )

    def send_place(self, protocol: MetaplaceProtocol) -> None:
        place = self.world.start_place
        if place is None:
            return
        presentation = self.presentation
        camera = presentation.camera
        camera3d = presentation.camera3d
        physics = presentation.physics

        protocol.send_tag(
            'P_MAPBLOCK', 't', 1, 1, presentation.mapblocks.tilemap or EMPTY_TILEMAP
        )
        protocol.send_tag(
            'P_MAPBLOCK', 'h', 1, 1, presentation.mapblocks.heightmap or EMPTY_HEIGHTMAP
        )
        protocol.send_tag('P_ZOOMLIMIT', *camera.zoom_lock)
        protocol.send_tag(
            'P_RENDERFLAGS', presentation.render.occlude_tiles, presentation.render.alpha_cutoff
        )
        protocol.send_tag('P_SIZE', place.width, place.height)
        protocol.send_tag('P_VIEW', camera.view_mode.value)
        protocol.send_tag('P_START', *presentation.start_position)
        protocol.send_tag('P_LOCKVIEW', camera.lock_view)
        protocol.send_tag('P_TILESIZE', camera.tile_size)
        protocol.send_tag('P_ELEVSCALE', camera.elevation_scale)
        protocol.send_tag('P_RELIEF', camera.terrain_lighting)
        protocol.send_tag(
            'P_LOCKSCROLL',
            camera.lock_scroll,
            camera.move_radius,
            camera.move_rate,
            camera.move_recenter,
        )
        protocol.send_tag('P_HEIGHTMAPSCALE', camera.height_map_scale)
        protocol.send_tag('P_HEIGHTMAPDIVISIONS', camera.height_map_divisions)
        protocol.send_tag(
            'P_CAMERA3D',
            camera3d.near,
            camera3d.far,
            *camera3d.position,
            *camera3d.angle,
            camera3d.camera_view,
            camera3d.left,
            camera3d.right,
            camera3d.top,
            camera3d.bottom,
            camera3d.aspect,
            camera3d.vertical_fov,
            camera3d.focal_length,
            0,
            camera3d.camera_width,
            camera3d.camera_height,
        )
        protocol.send_tag('UI_BGCOLOR', 255, 255, 255)
        protocol.send_tag('P_DRAG', presentation.draggable)
        protocol.send_tag('P_CAMLIMITS', *camera.margin_top_left, *camera.margin_bottom_right)
        protocol.send_tag('P_LOCKRENDERSIZE', 0, camera3d.camera_width, camera3d.camera_height)
        protocol.send_tag('P_LOCKOBJECTS', presentation.object_lock)
        protocol.send_tag(
            'P_PHYSICS',
            physics.gravity,
            physics.collision,
            physics.friction,
            physics.tile_friction,
            physics.safety_net,
            physics.net_height,
            physics.net_friction,
            physics.net_bounce,
        )
        protocol.send_tag('P_ASSETSCOMPLETE', 0, 0)

    @staticmethod
    def send_avatar_data(protocol: MetaplaceProtocol, player_id: int) -> None:
        # TODO: Add metaplace plugin system to decouple the base metaplace server from the app-specific events
        animation_paths = {
            'Marshmellow': '<base_asset_url>avatar/transformations/marshmellow/en_US/deploy/animation/all_platforms/all/',
            'Olaf': '<base_asset_url>avatar/transformations/olaf/en_US/deploy/animation/all_platforms/all/',
            'penguin': '<base_asset_url>avatar/penguin/en_US/deploy/animation/all_platforms/all/',
            'puffle': '<base_asset_url>avatar/puffle/en_US/deploy/animation/all_platforms/all/',
        }
        avatar_data = {
            'character': 'penguin',
            'schemaJson': '<base_asset_url>avatar/jsonData/transformation_schema.json',
            'shadow': '<base_asset_url>avatar/penguin/en_US/deploy/mesh/all_platforms/penguin_shadow.mmf',
            'shadowFriend': '<base_asset_url>avatar/penguin/en_US/deploy/mesh/all_platforms/penguin_shadowGreen.mmf',
            'shadowSelf': '<base_asset_url>avatar/penguin/en_US/deploy/mesh/all_platforms/penguin_shadowBlue.mmf',
            'url': '<base_asset_url>avatar/penguin/en_US/deploy/mesh/all_platforms/penguin.mmf',
            'zoom': '0.7',
        }
        protocol.session.send_client_event(
            player_id,
            'setAnimPaths',
            animation_paths,
        )
        protocol.session.send_client_event(
            player_id,
            'setAvatarLoadingData',
            avatar_data,
        )

    def reject_login(self, protocol: MetaplaceProtocol) -> None:
        self.logger.warning('Rejecting login for player %s', protocol.session.player_id)
        protocol.send_tag('S_LOGINDEBUG', 'user code 900')
        protocol.close_connection()

class MetaplaceWorldServer:
    """Runs a Twisted metaplace factory."""

    def __init__(
        self,
        factory: Factory,
        port: int,
        interface: str = '0.0.0.0',
    ) -> None:
        self.factory = factory
        self.port = port
        self.interface = interface
        self.logger = logging.getLogger('metaplace.server')

        self._listener: IListeningPort | None = None

    def run(self) -> None:
        if self._listener is not None:
            raise RuntimeError('Metaplace world server has already been started')

        self._listener = reactor.listenTCP(
            self.port, # type: ignore
            self.factory, # type: ignore
            interface=self.interface,
        )

        self.logger.info(
            'Metaplace world server listening on %s:%s',
            self.interface,
            self.port,
        )
        reactor.run() # type: ignore
