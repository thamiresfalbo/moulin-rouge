import numpy as np
from numpy.typing import NDArray
import scipy.signal
import attrs
from copy import copy


@attrs.define
class MMap:
    width: int
    height: int
    _tiles: NDArray[np.uint8] = attrs.field(init=False)
    _fill_percentage: float = attrs.field(init=False, default=0.45)

    def __attrs_post_init__(self):
        self._tiles: NDArray[np.uint8] = np.zeros((self.height, self.width))

    def add_borders(self):
        self._tiles[[0, -1], :] = 0
        self._tiles[:, [0, -1]] = 0

    def build(self):
        """Returns the cave as an numpy array. Note that the arrays have inverted coordinates(y, x)"""
        return self._tiles

    def make_caves(self):
        """Default method for cave-making."""
        return self

    def print_caves(self):
        for i in range(self.height):
            for j in range(self.width):
                if self._tiles[i, j] == 2:
                    print(" ", end="")
                else:
                    print("#", end="")
            print()

    def out_of_bounds(self, x: int, y: int):
        if x < 2 or x >= self.width - 2 or y < 2 or y >= self.height - 2:
            return True
        return False

    def is_wall(self, x: int, y: int) -> bool:
        if self._tiles[y, x] == 1:
            return True
        return False


# CELLULAR AUTOMATA
# I ended using the latter since looping was slow.
# http://trystans.blogspot.com/2011/08/roguelike-tutorial-03-scrolling-through.html
# https://roguebasin.com/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
# https://github.com/libtcod/python-tcod/blob/main/examples/cavegen.py
class MCellularAutomata(MMap):
    """A natural cave-looking map."""

    def __attrs_post_init__(self):
        self._tiles: NDArray[np.uint8] = (
            np.random.random((self.height, self.width)) > self._fill_percentage
        )

    def __middle_corridors(self):
        mid_y = int(self.height / 2)
        mid_x = int(self.width / 2)
        factor = 2
        self._tiles[mid_y - factor : mid_y, :] = 1
        self._tiles[:, mid_x - factor : mid_x] = 1

    def make_caves(self):
        self.__middle_corridors()
        for _ in range(5):
            self._tiles = self.convolve(self._tiles)
            self.add_borders()

        return self

    def convolve(self, tiles: NDArray[np.uint8]):
        neighbors: NDArray[np.uint8] = scipy.signal.convolve2d(
            tiles == 0, [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "same"
        )
        next_tiles = neighbors < 5

        return next_tiles


# RANDOM WALK
class RandomWalk(MMap):
    """A map made by random dwarves."""

    def make_caves(self):
        goal = int(self._tiles.size * self._fill_percentage)
        total_tiles = 0
        steps = 400

        center = [int(self._tiles / 2), int(self._tiles[0] / 2)]
        self._tiles[center[0], center[1]] = 1
        drunk_y = copy(center[0])
        drunk_x = copy(center[1])
        while total_tiles < goal:
            total_tiles = np.count_nonzero(self._tiles)

            for _ in range(steps):
                r = np.random.randint(5)
                if r == 4:
                    drunk_x += 1
                elif r == 3:
                    drunk_x -= 1
                elif r == 2:
                    drunk_y += 1
                elif r == 1:
                    drunk_y -= 1

                if self.out_of_bounds(drunk_x, drunk_y):
                    drunk_x = center[1]
                    drunk_y = center[0]
                self._tiles[drunk_y, drunk_x] = 1

        self.add_borders()
        return self
