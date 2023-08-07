import constants
import numpy as np


graphic_dt = np.dtype([("ch", np.int32), ("fg", "3B"), ("bg", "3B")])

tile_dt = np.dtype([("walkable", bool), ("transparent", bool), ("dark", graphic_dt)])


def new_tile(
    walkable: bool,
    transparent: bool,
    dark: tuple[int, tuple[int, int, int], tuple[int, int, int]],
):
    return np.array((walkable, transparent, dark), dtype=tile_dt)


WALL = new_tile(
    walkable=False,
    transparent=True,
    dark=(0x2592, constants.PURPLE, constants.BLACK),
)

FLOOR = new_tile(
    walkable=True,
    transparent=True,
    dark=(0x20, constants.PURPLE, constants.BLACK),
)
