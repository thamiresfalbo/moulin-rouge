import tcod
import numpy as np
from numpy.typing import NDArray
from world.world import World

# Inspired by this tutorial(in Java):
# http://trystans.blogspot.com/2011/08/roguelike-tutorial-03-scrolling-through.html
# https://roguebasin.com/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
class CellularAutomata(World):
    """A natural cave-looking map."""

    def make_caves(self):
        self.__randomize_tiles()
        self.__smooth_caves(8)
        return self

    def print_caves(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x,y]:
                    print('#',end='')
                else:
                    print('.',end='')

    def __randomize_tiles(self) -> None:
        self.tiles = np.random.random((self.width,self.height)) > 0.45


    def __smooth_caves(self, times:int) -> None:
        """Check the neighbour tiles(3x3). A tile becomes a wall if there are 5 walls in the region."""
        tiles2 = np.empty(shape=[self.width,self.height], dtype=np.bool_ , order='F')
        for time in range(times):
            for x in range(self.width):
                for y in range(self.height):
                    # Check if out of bounds
                    #TODO: There is a problem here.
                    if x == 0 or x == self.width -1 or y == 0 or y == self.height - 1:
                        tiles2[x][y] = True
                    else:
                        tiles2[x][y] = self.__is_wall(tiles2, x, y)
        self.tiles = np.copy(tiles2, order='F')

    def __is_wall(self, tiles: NDArray[np.bool_], x: int, y:int) -> bool:
        m = []
        m.append(tiles[x-1,y-1:3])
        m.append(tiles[x, y-1:3])
        m.append(tiles[x+1, y-1:3])
        return np.count_nonzero(m) < 5

    def __flood_fill(self):
        """Connect isolated caves."""
        pass
