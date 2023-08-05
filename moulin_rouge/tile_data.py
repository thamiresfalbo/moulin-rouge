import attrs
import constants


@attrs.define
class Tile:
    char: str
    walkable: bool
    transparent: bool
    fg: tuple[int, int, int]


ROCK = Tile(" ", walkable=False, transparent=False, fg=constants.WHITE)
FLOOR = Tile(".", walkable=True, transparent=True, fg=constants.WHITE)
WALL = Tile("#", walkable=False, transparent=False, fg=constants.WHITE)
STAIRS_UP = Tile("<", walkable=True, transparent=True, fg=constants.YELLOW)
STAIRS_DOWN = Tile(">", walkable=True, transparent=True, fg=constants.YELLOW)
