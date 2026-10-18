
from app.metaplace import (
    Camera,
    Camera3D,
    InputBinding,
    InputTarget,
    InputType,
    MapBlocks,
    Place,
    PlacePresentation,
    World,
    WorldCatalog,
)
import config

CLIENT_VERSION = 'FY15-20150206 (4954)r'
BASE_ASSET_URL = ' '
TOWN_PLACE_ID = '0:205790002'
TOWN_PLACE_OBJECT_ID = 2

EMPTY_TILEMAP = (
    'iVBORw0KGgoAAAANSUhEUgAAAEAAAAAoCAAAAABrpaM1AAAANElEQVRIiWNgGAWjYBSMghEJ'
    'GEEAhzAc4BDGqoSgykFrALo55BoAN2XUgFEDiM+Jo2BQAwDdDQLtiDfyPgAAAABJRU5ErkJggg=='
)
EMPTY_HEIGHTMAP = (
    'iVBORw0KGgoAAAANSUhEUgAAAEEAAAApCAAAAABPOxuuAAAAIklEQVRIie3MIQEAAAACIKc7'
    '3RFWGED6isFgMBgMBoPBcBgfzjTMSGY6zQAAAABJRU5ErkJggg=='
)

def create_world() -> World:
    world = World(
        world_id=config.METAPLACE_WORLD_ID,
        name=config.METAPLACE_WORLD_NAME,
        owner=config.METAPLACE_WORLD_OWNER,
        stylesheet_id=config.METAPLACE_STYLESHEET_ID,
        start_place_id=f'0:{config.METAPLACE_START_PLACE_ID}',
    )
    place = Place(
        place_id=TOWN_PLACE_ID,
        name='clubpenguin_town',
        width=64,
        height=40,
    )
    world.add_place(place)
    world.set_entry_place(place.place_id, object_id=TOWN_PLACE_OBJECT_ID)
    return world

def create_world_catalog() -> WorldCatalog:
    catalog = WorldCatalog()
    world = catalog.add_world(create_world())
    catalog.map_place('clubpenguin', 'clubpenguin_town_en_US', world)
    catalog.map_place('clubpenguin', 'clubpenguin_town_en_3', world)
    return catalog

def create_place_presentation() -> PlacePresentation:
    return PlacePresentation(
        mapblocks=MapBlocks(
            tilemap=EMPTY_TILEMAP,
            heightmap=EMPTY_HEIGHTMAP,
        ),
        camera=Camera(
            position=(32, 20, 0),
            tile_size=16,
            elevation_scale=0.03125,
            lock_camera=True,
            lock_zoom=True,
            height_map_scale=0.078125,
        ),
        camera3d=Camera3D(
            camera_width=1024,
            camera_height=640,
        ),
        inputs=(
            InputBinding(
                'use',
                '0:10',
                InputTarget.GOB,
                InputType.MOUSE_CLICK,
                'use'
            ),
            InputBinding(
                'touch-the-terrain',
                '0:8600033',
                InputTarget.TILE,
                InputType.MOUSE_UP,
                'path_terrain',
            ),
            InputBinding(
                'mouse-the-terrain',
                '0:8600033',
                InputTarget.TILE,
                InputType.MOUSE_CLICK,
                'path_terrain',
            ),
        ),
        start_position=(3, 7, 0),
        player_art_id='0:2480001',
        player_template_id='0:1',
    )
