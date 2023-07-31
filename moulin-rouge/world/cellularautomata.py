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
        tiles2: NDArray[np.bool_] = np.copy(tiles)
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                walls = self.__adjacent_walls(self.tiles, y, x)
                if tiles2[y, x] == 0 and walls >= 4:
                    tiles2[y, x] == 0
                elif tiles2[y, x] == 1 and walls >= 5:
                    tiles2[y, x] == 0
                else:
                    tiles2[y, x] = 1
        return tiles2

    def __adjacent_walls(self, tiles: NDArray[np.bool_], y: int, x: int) -> int:
        walls = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if tiles[j][i] == False:
                    walls += 1
        return walls

    def __flood_fill(self, tiles: NDArray[np.bool_]) -> NDArray[np.bool_]:
        pass
