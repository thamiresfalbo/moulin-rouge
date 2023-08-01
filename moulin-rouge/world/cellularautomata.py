# http://trystans.blogspot.com/2011/08/roguelike-tutorial-03-scrolling-through.html
# https://roguebasin.com/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
# TODO: Add flood fill algorithm
# TODO: Make tile dtypes
import numpy as np
from numpy.typing import NDArray
from world.world import World


class CellularAutomata(World):
    """A natural cave-looking map."""

    def __init__(self, height: int, width: int) -> None:
        super().__init__(width, height)
        # Keep common values for CA generation: 45% fill with 4 iterations.
        self.probability: float = 0.45
        self.times: int = 4
        self.tiles: NDArray[np.bool_] = (
            np.random.random(size=(self.height, self.width)) > self.probability
        )

    def build(self) -> NDArray[np.bool_]:
        """
        Builds the CA map and returns it as a numpy array.
        Note that the arrays have inverted coordinates(y, x)!
        """
        for _ in range(self.times):
            self.tiles = self.__make_caves(self.tiles)
            self.tiles[[0, -1], :] = 0
            self.tiles[:, [0, -1]] = 0

        return self.tiles

    def print_caves(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.tiles[i, j] == True:
                    print(" ", end="")
                else:
                    print("#", end="")
            print()

    def __make_caves(self, tiles: NDArray[np.bool_]) -> None:
        """
        Picks an 3x3 area with the tile centered on it.
        If there are 5 or more walls around, the tile becomes a wall.
        If there are 2 or less walls around, the tile becomes a floor.
        """
        tiles2: NDArray[np.bool_] = np.copy(tiles)
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                adjacent = self.__adjacent_walls(self.tiles, y, x)
                if adjacent >= 5:
                    tiles2[y, x] = 0
                elif adjacent <= 2:
                    tiles2[y, x] = 1
                else:
                    tiles2[y, x] = 1

        return tiles2

    def __adjacent_walls(self, tiles: NDArray[np.bool_], y: int, x: int) -> int:
        adjacent = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if tiles[j][i] == False and not (j == 0 and i == 0):
                    adjacent += 1
        return adjacent

    def __neighbor_walls(self, tiles: NDArray[np.bool_], y: int, x: int) -> int:
        neighbor = 0
        for j in range(y - 2, y + 3):
            for i in range(x - 2, x + 3):
                if i - x == 2 and j - y == 2:
                    continue
                if i < 0 or y < 0 or i >= self.width or j >= self.height:
                    continue
                if tiles[j, i] == True and not (j == 0 and i == 0):
                    neighbor += 1
        return neighbor

    def __flood_fill(self, tiles: NDArray[np.bool_]) -> NDArray[np.bool_]:
        """
        Uses an breadth-fill algorithm to check for isolated caves.
        If the open area is smaller than 45%, start again.
        """
        pass
