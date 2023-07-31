import numpy as np
from numpy.typing import NDArray
from world.world import World


# https://roguebasin.com/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
class CellularAutomata(World):
    """A natural cave-looking map."""

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.tiles = np.random.random((self.width, self.height)) < 0.40

    def print_caves(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x, y]:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def make_caves(self, times: int = 3):
        """
        Check the neighbour tiles(3x3). A tile becomes a wall if there are 5 walls in the region.
        Walls are false values.
        Floors are true values.
        """
        tiles2 = np.zeros(shape=[self.width, self.height], dtype=np.bool_, order="F")
        for _ in range(times):
            for x in range(1, self.width - 1):
                for y in range(1, self.height - 1):
                    if self.tiles[x, y] == False:
                        self.tiles[x, y] = self.__place_wall(self.tiles, x, y) < 4

        # self.tiles = np.ndarray.copy(tiles2, order="F")

    def __place_wall(self, tiles: NDArray[np.bool_], x: int, y: int):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if tiles[x + i][y + j] == False and not (i == 0 and j == 0):
                    count += 1
        return count

    def __flood_fill(self):
        """Connect isolated caves."""
        pass
