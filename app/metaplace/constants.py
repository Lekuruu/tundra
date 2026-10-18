
from enum import Enum, IntEnum

class InputType(IntEnum):
    UP                 = 1
    DOWN               = 2
    MOUSE_CLICK        = 3
    MOUSE_BOX          = 4
    MOUSE_DOUBLE_CLICK = 5
    MOUSE_UP           = 6

class InputModifier(IntEnum):
    NONE  = 0
    SHIFT = 1
    CTRL  = 2
    ALT   = 3

class InputTarget(IntEnum):
    TILE = 1
    GOB  = 2

class ServerType(IntEnum):
    LIVE = 0
    DEV  = 1

class BuildType(IntEnum):
    DEBUG   = 0
    RELEASE = 1
    PROFILE = 2
    MEMORY  = 3

class MirrorMode(IntEnum):
    NONE = 0
    X = 1
    Y = 2
    XY = 3

class OriginMode(IntEnum):
    NONE = 0
    CENTER = 1
    BOTTOM_MIDDLE = 2
    TOP_LEFT = 3

class ViewMode(IntEnum):
    OVERHEAD = 0
    OVERHEAD_ROTATED = 1
    ISO_STEPPED = 2
    ISO_SLOPED = 3
    ISO = 4
    SIDE = 5
    VIEW_3D = 6
    FREE = 7

class MapblockType(str, Enum):
    HEIGHTMAP = "h"
    TILEMAP = "t"
    MAP = "ht"
