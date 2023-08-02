import numpy as np
from numpy.typing import NDArray
import scipy.signal
from copy import copy
from attrs import define, field


@define
class MMap:
    """
    Main template class for maps.
    """

    width: int
    height: int
    tiles: NDArray[np.uint8] = field(init=False)
    _fill_percentage: float = field(init=False, default=0.45)
    _center_x: int = field(init=False)
    _center_y: int = field(init=False)

    def __attrs_post_init__(self):
        self.tiles: NDArray[np.uint8] = np.zeros((self.height, self.width))
        self._center_x = int(len(self.tiles) / 2)
        self._center_y = int(len(self.tiles[0]) / 2)

    def add_borders(self):
        self.tiles[[0, -1], :] = 0
        self.tiles[:, [0, -1]] = 0

    def build(self):
        """Returns the cave as an numpy array. Note that the arrays have inverted coordinates(y, x)"""
        return self.tiles

    def make_caves(self):
        """Default method for cave-making."""
        return self

    def print_caves(self):
        for j in range(self.height):
            for i in range(self.width):
                if self.tiles[j, i] == 2:
                    print(" ", end="")
                else:
                    print("#", end="")
            print()

    def out_of_bounds(self, x: int, y: int):
        if x < 2 or x >= self.width - 2 or y < 2 or y >= self.height - 2:
            return True
        return False

    def is_wall(self, x: int, y: int) -> bool:
        if self.tiles[y, x] == 1:
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
        self.tiles: NDArray[np.uint8] = (
            np.random.random((self.height, self.width)) > self._fill_percentage
        )
        self._center_x = int(len(self.tiles) / 2)
        self._center_y = int(len(self.tiles[0]) / 2)

    def __middle_corridors(self):
        factor = 2
        self.tiles[self._center_y - factor : self._center_y, :] = 1
        self.tiles[:, self._center_x - factor : self._center_x] = 1

    def make_caves(self):
        self.__middle_corridors()
        for _ in range(5):
            self.tiles = self.convolve(self.tiles)
            self.add_borders()

        return self

    def convolve(self, tiles: NDArray[np.uint8]):
        neighbors: NDArray[np.uint8] = scipy.signal.convolve2d(
            tiles == 0, [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "same"
        )
        next_tiles = neighbors < 5

        return next_tiles


# RANDOM WALK
class MRandomWalk(MMap):
    """A map made by random dwarves."""

    def make_caves(self):
        goal = int(self.tiles.size * self._fill_percentage)
        total_tiles = 0
        steps = 400

        self.tiles[self._center_y, self._center_x] = 1
        drunk_y = copy(self._center_y)
        drunk_x = copy(self._center_x)
        while total_tiles < goal:
            total_tiles = np.count_nonzero(self.tiles)

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
                    drunk_x = self._center_x
                    drunk_y = self._center_y
                self.tiles[drunk_y, drunk_x] = 1

        self.add_borders()
        return self
