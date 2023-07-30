import tcod
import numpy as np
from world.world import World
import random

# Inspired by this tutorial(in Java):
# http://trystans.blogspot.com/2011/08/roguelike-tutorial-03-scrolling-through.html
# https://roguebasin.com/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
class CellularAutomata(World):
    """A natural cave-looking map."""
    def make_caves(self):
        self.__randomize_tiles(self.tiles)
        # self.__smooth_caves()
        return self


    def __randomize_tiles(self, tiles) -> None:
        for x in range(len(tiles)):
            for y in range(len(tiles[x])):
                if random.random() < 0.4:
                    tiles[x][y] = 0
                else:
                    tiles[x][y] = 1


    def __smooth_caves(self, times:int = 8) -> None:
        """Check the neighbour tiles(3x3). A tile becomes a wall if there are 5 walls in the region."""
        tiles2 = np.empty(shape=[self.width,self.height], dtype=np.bool_ , order='F')
        for time in range(times):
            for x in range(self.width):
                for y in range(self.height):
                    if x == 0 or x == self.width -1 or y == 0 or y == self.height - 1:
                        tiles2[x][y] = 1
                    else:
                        tiles2[x][y] = self.__wall_logic(tiles2, x, y)
        self.tiles = np.copy(tiles2)

    def __count_nearby_tiles(self, tiles: np.ndarray, x: int, y:int) -> int:
        m = []
        for i in range(x-1, x+1):
            m.ap


    def __wall_logic(self, tiles, x: int, y:int) -> bool:
        return self.__count_nearby_tiles(tiles,x,y) >= 5

    def __flood_fill(self):
        """Connect isolated caves."""
        pass


