
from dataclasses import dataclass, field

from .world import Place, PlaceInstance
from .constants import ViewMode

@dataclass(slots=True)
class MapBlocks:
    tilemap: str = ''
    heightmap: str = ''

@dataclass(slots=True)
class Render:
    alpha_cutoff: int = 48
    occlude_tiles: bool = False

@dataclass(slots=True)
class Camera:
    position: tuple[float, float, float] = (0, 0, 0)
    view_mode: ViewMode = ViewMode.SIDE
    tile_size: int = 64
    elevation_scale: float = -1
    terrain_lighting: bool = True
    lock_view: bool = False
    lock_camera: bool = False
    lock_zoom: bool = False
    lock_scroll: bool = True
    zoom: float = 1
    zoom_lock: tuple[int, int] = (-1, -1)
    move_radius: int = 0
    move_rate: int = 0
    move_recenter: int = 0
    height_map_divisions: int = 1
    height_map_scale: float = 0.5
    margin_top_left: tuple[int, int] = (0, 0)
    margin_bottom_right: tuple[int, int] = (0, 0)

@dataclass(slots=True)
class Camera3D:
    near: int = 0
    far: int = 0
    position: tuple[float, float, float] = (0, 0, 0)
    angle: tuple[float, float, float] = (0, 0, 0)
    camera_view: int = 0
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0
    aspect: int = 0
    vertical_fov: int = 0
    focal_length: int = 864397819904
    camera_width: int = 1024
    camera_height: int = 768

@dataclass(slots=True)
class Physics:
    gravity: bool = False
    collision: bool = False
    friction: bool = False
    tile_friction: bool = False
    safety_net: bool = False
    net_height: int = 0
    net_friction: bool = False
    net_bounce: bool = True

@dataclass(slots=True)
class PlacePresentation:
    """Optional rendering data kept outside the place's domain identity."""

    mapblocks: MapBlocks = field(default_factory=MapBlocks)
    render: Render = field(default_factory=Render)
    camera: Camera = field(default_factory=Camera)
    camera3d: Camera3D = field(default_factory=Camera3D)
    physics: Physics = field(default_factory=Physics)
    start_position: tuple[float, float, float] = (0, 0, 0)
    draggable: bool = False
    object_lock: bool = False

__all__ = (
    'Camera',
    'Camera3D',
    'MapBlocks',
    'Physics',
    'Place',
    'PlaceInstance',
    'PlacePresentation',
    'Render',
)
