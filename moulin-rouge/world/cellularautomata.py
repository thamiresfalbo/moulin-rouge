import numpy as np
from numpy.typing import NDArray
from world.world import World


# http://trystans.blogspot.com/2011/08/roguelike-tutorial-03-scrolling-through.html
# https://roguebasin.com/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
class CellularAutomata(World):
    """A natural cave-looking map."""

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.probability: float = 0.45
        self.times: int = 4
        self.tiles = np.random.random((self.width, self.height)) > self.probability

    def make_caves(self) -> None:
        """Check the neighbour tiles(3x3). A tile becomes a wall if there are 5 walls in the region."""
        tiles2 = np.zeros(shape=[self.width, self.height], dtype=np.bool_, order="F")
        for _ in range(self.times):
            for x in range(1, self.width - 1):
                for y in range(1, self.height - 1):
                    count = self.__place_wall(self.tiles, x, y)
                    if count < 5:
                        tiles2[x, y] = True

        self.tiles = np.ndarray.copy(tiles2, order="F")

    def __place_wall(self, tiles: NDArray[np.bool_], x: int, y: int) -> int:
        count = 0

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if tiles[i][j] == False and not (i == 0 and j == 0):
                    count += 1

        return count

    def __clear_isolated(self) -> None:
        """Clean isolated cells"""
        pass

    def __flood_fill(self) -> None:
        """Connect isolated caves."""
        pass
