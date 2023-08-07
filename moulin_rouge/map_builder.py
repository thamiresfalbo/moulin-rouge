import numpy as np
from numpy.typing import NDArray
import scipy.signal
from copy import copy
from attrs import define, field
import tcod.bsp
import tcod.los
import tile_data
from typing import Any
import random


@define
class MMap:
    """Main template class for maps."""

    width: int
    height: int
    tiles: NDArray[Any] = field(init=False)
    _fill_percentage: float = field(init=False, default=0.45)
    _center_x: int = field(init=False)
    _center_y: int = field(init=False)

    def __attrs_post_init__(self):
        self.tiles = np.full(
            shape=(self.height, self.width),
            fill_value=tile_data.WALL,
            order="F",
        )
        self._center_x = int(len(self.tiles) / 2)
        self._center_y = int(len(self.tiles[0]) / 2)

    def add_borders(self):
        self.tiles[[0, -1], :] = tile_data.WALL
        self.tiles[:, [0, -1]] = tile_data.WALL

    def build(self):
        """Returns the cave as an numpy array."""
        return self.tiles

    def make_caves(self):
        """Default method for cave-making."""
        return self

    def print_caves(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.tiles[i, j] == 1:
                    print(" ", end="")
                else:
                    print("#", end="")
            print()

    def out_of_bounds(self, x: int, y: int):
        if x < 2 or x >= self.width - 2 or y < 2 or y >= self.height - 2:
            return True
        return False

    def is_wall(self, x: int, y: int):
        if self.tiles[x, y] == tile_data.WALL:
            return True
        return False


# CELLULAR AUTOMATA
class MCellularAutomata(MMap):
    """A natural cave-looking map."""

    def middle_corridors(self):
        factor = 2
        self.tiles[self._center_x - factor : self._center_x, :] = tile_data.FLOOR
        self.tiles[:, self._center_y - factor : self._center_y] = tile_data.FLOOR

    def randomize_tiles(self):
        for i in range(self.width):
            for j in range(self.height):
                if random.random() > self._fill_percentage:
                    self.tiles[i][j] == tile_data.FLOOR
                else:
                    self.tiles[i][j] == tile_data.WALL

    def make_caves(self):
        self.randomize_tiles()
        self.middle_corridors()
        for _ in range(5):
            self.tiles = self.convolve(self.tiles)
            self.add_borders()
        return self

    # TODO Replace scipy implementation for MCellularAutomata
    def convolve(self, tiles):
        tiles2 = []
        return tiles2


# RANDOM WALK
class MRandomWalk(MMap):
    """A map made by umber hulks."""

    def make_caves(self):
        goal = int(self.tiles.size * self._fill_percentage)
        total_tiles = 0
        steps = 400

        center_x = int(len(self.tiles[0]) / 2)
        center_y = int(len(self.tiles) / 2)
        self.tiles[center_y, center_x] = 1
        drunk_y = copy(center_y)
        drunk_x = copy(center_x)
        while total_tiles < goal:
            total_tiles = np.count_nonzero(self.tiles == tile_data.FLOOR)

            for _ in range(steps):
                r = np.random.randint(5)
                match r:
                    case 4:
                        drunk_x += 1
                    case 3:
                        drunk_x -= 1
                    case 2:
                        drunk_y += 1
                    case 1:
                        drunk_y -= 1

                if self.out_of_bounds(drunk_x, drunk_y):
                    drunk_x = center_x
                    drunk_y = center_y
                self.tiles[drunk_y, drunk_x] = tile_data.FLOOR

        self.add_borders()
        return self


# TODO Implement MRogue Class
# ROGUE DUNGEON
class MRogue(MMap):
    """The classic nine-room map."""

    def make_caves(self):
        return self
