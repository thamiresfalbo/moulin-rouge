import numpy as np
from numpy.typing import NDArray
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
    fill_percentage: float = field(init=False, default=0.45)
    center_x: int = field(init=False)
    center_y: int = field(init=False)

    def __attrs_post_init__(self):
        self.tiles = np.full(
            shape=(self.height, self.width),
            fill_value=tile_data.WALL,
            order="F",
        )
        self.center_x = int(len(self.tiles) / 2)
        self.center_y = int(len(self.tiles[0]) / 2)

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
        self.tiles[self.center_x - factor : self.center_x, :] = tile_data.FLOOR
        self.tiles[:, self.center_y - factor : self.center_y] = tile_data.FLOOR

    def randomize_tiles(self):
        rng = np.random.default_rng()
        self.tiles = rng.choice(
            a=[tile_data.WALL, tile_data.FLOOR],
            size=(self.width, self.height),
            p=[self.fill_percentage, 1.0 - self.fill_percentage],
        )

    def make_caves(self):
        self.randomize_tiles()
        self.middle_corridors()
        for _ in range(5):
            self.tiles = self.convolve(self.tiles)
            self.add_borders()
        return self

    def convolve(self, tiles):
        tiles2 = np.copy(tiles)
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                adjacent = self.adjacent_walls(tiles, x, y)
                if adjacent >= 5:
                    tiles2[x, y] = tile_data.WALL
                elif adjacent <= 2:
                    tiles2[x, y] = tile_data.FLOOR
                else:
                    tiles2[x, y] = tile_data.FLOOR

        return tiles2

    def adjacent_walls(self, tiles: NDArray[np.bool_], x: int, y: int) -> int:
        adjacent = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if tiles[i, j] == tile_data.WALL and not (j == 0 and i == 0):
                    adjacent += 1
        return adjacent


# RANDOM WALK
class MRandomWalk(MMap):
    """A map made by umber hulks."""

    def make_caves(self):
        goal = int(self.tiles.size * self.fill_percentage)
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
