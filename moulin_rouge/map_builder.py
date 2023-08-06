import numpy as np
from numpy.typing import NDArray
import scipy.signal
from copy import copy
from attrs import define, field
import tcod.bsp
import tcod.los


@define
class MMap:
    """Main template class for maps."""

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


class MCellularAutomata(MMap):
    """A natural cave-looking map."""

    def __middle_corridors(self):
        factor = 2
        self.tiles[self._center_y - factor : self._center_y, :] = 1
        self.tiles[:, self._center_x - factor : self._center_x] = 1

    def make_caves(self):
        self.tiles: NDArray[np.uint8] = (
            np.random.random((self.height, self.width)) > self._fill_percentage
        )
        self.__middle_corridors()
        for _ in range(5):
            self.tiles = self.convolve(self.tiles)
            self.add_borders()

        return self

    # TODO Replace scipy implementation for MCellularAutomata
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

        center_x = int(len(self.tiles[0]) / 2)
        center_y = int(len(self.tiles) / 2)
        self.tiles[center_y, center_x] = 1
        drunk_y = copy(center_y)
        drunk_x = copy(center_x)
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
                    drunk_x = center_x
                    drunk_y = center_y
                self.tiles[drunk_y, drunk_x] = 1

        self.add_borders()
        return self


class MRogue(MMap):
    def make_caves(self):
        return self
