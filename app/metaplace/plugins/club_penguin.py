
from app.metaplace import (
    GameObject,
    MetaplacePlugin,
    MetaplaceProtocol,
)

class CompanionAppPlugin(MetaplacePlugin):
    """Adds player behavior for the club penguin companion app to a metaplace world."""

    def on_player_ready(
        self,
        protocol: MetaplaceProtocol,
        player: GameObject,
    ) -> None:
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
            player.object_id,
            'setAnimPaths',
            animation_paths
        )
        protocol.session.send_client_event(
            player.object_id,
            'setAvatarLoadingData',
            avatar_data,
        )
