# TODO: Add flood fill algorithm
# TODO: Make tile dtypes
import numpy as np
from numpy.typing import NDArray
from map.map_architect import MapArchitect
import scipy.signal


# I ended using the latter since looping was slow.
# http://trystans.blogspot.com/2011/08/roguelike-tutorial-03-scrolling-through.html
# https://roguebasin.com/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
# https://github.com/libtcod/python-tcod/blob/main/examples/cavegen.py
class CellularAutomata(MapArchitect):
    """A natural cave-looking map."""

    def __init__(self, height: int, width: int) -> None:
        super().__init__(width, height)
        self.probability: float = 0.43
        self.times: int = 5
        self.tiles: NDArray[np.uint8] = (
            np.random.random(size=(self.height, self.width)) > self.probability
        )

    def build(self) -> NDArray[np.uint8]:
        """
        Builds the CA map and returns it as a numpy array.
        Note that the arrays have inverted coordinates(y, x)!
        """
        self.__middle_corridors()
        for _ in range(self.times):
            self.tiles = self.__make_caves(self.tiles)
            self.tiles[[0, -1], :] = 0
            self.tiles[:, [0, -1]] = 0

        return self.tiles

    def print_caves(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.tiles[i, j] == 2:
                    print(" ", end="")
                else:
                    print("#", end="")
            print()

    def __middle_corridors(self):
        mid_y = int(self.height / 2)
        mid_x = int(self.width / 2)
        factor = 2
        self.tiles[mid_y - factor : mid_y, :] = 1
        self.tiles[:, mid_x - factor : mid_x] = 1

    def __make_caves(self, tiles: NDArray[np.uint8]):
        tiles2: NDArray[np.uint8] = scipy.signal.convolve2d(
            tiles == 0, [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "same"
        )

        return tiles2 < 5
