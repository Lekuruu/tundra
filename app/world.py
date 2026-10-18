
from app.protocols.metaplace import (
    PlacePresentation,
    Place,
    WorldCatalog,
    World,
    Camera3D,
    Camera
)
import config

def create_world() -> World:
    world = World(
        world_id=config.METAPLACE_WORLD_ID,
        name=config.METAPLACE_WORLD_NAME,
        owner=config.METAPLACE_WORLD_OWNER,
        stylesheet_id=config.METAPLACE_STYLESHEET_ID,
    )
    world.add_place(Place(
        place_id=config.METAPLACE_START_PLACE_ID,
        name='clubpenguin_town',
        width=64,
        height=40,
    ), start=True)
    return world

def create_world_catalog() -> WorldCatalog:
    catalog = WorldCatalog()
    world = catalog.add_world(create_world())
    catalog.map_place('clubpenguin', 'clubpenguin_town_en_US', world)
    return catalog

def create_place_presentation() -> PlacePresentation:
    return PlacePresentation(
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
        start_position=(3, 7, 0),
    )
