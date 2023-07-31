import numpy as np
from numpy.typing import NDArray
from world.world import World
from typing import Any
import scipy.signal


# http://trystans.blogspot.com/2011/08/roguelike-tutorial-03-scrolling-through.html
# https://roguebasin.com/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
class CellularAutomata(World):
    """A natural cave-looking map."""

    def __init__(self, height: int, width: int) -> None:
        super().__init__(width, height)
        self.probability: float = 0.6
        self.times: int = 8
        self.tiles: NDArray[np.bool_] = (
            np.random.random(size=(self.height, self.width)) > self.probability
        )

    def make_caves(self) -> None:
        """Check the neighbour tiles(3x3). A tile becomes a wall if there are 5 walls in the region."""
        tiles2: NDArray[np.bool_] = np.empty(shape=[self.height, self.width])
        for _ in range(self.times):
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    walls = self.__adjacent_walls(self.tiles, y, x)
                    tiles2[y, x] = walls["adjacent"] >= 5 or walls["neighbours"] <= 2

        self.tiles = np.copy(tiles2)

    def __adjacent_walls(self, tiles: NDArray[np.bool_], y: int, x: int):
        walls = {"adjacent": 0, "neighbours": 0}
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if tiles[j][i] == False:
                    walls["adjacent"] += 1

        for j in range(y - 2, y + 3):
            for i in range(x - 2, x + 3):
                if y - j == 2 or j >= self.height or x - i == 2 or i >= self.width:
                    continue
                if tiles[j][i] == False:
                    walls["neighbours"] += 1
        return walls

    def print_caves(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.tiles[i, j] == True:
                    print(" ", end="")
                else:
                    print("#", end="")
            print()
