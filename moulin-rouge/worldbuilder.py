# Inspired by this tutorial(in Java):
# http://trystans.blogspot.com/2011/08/roguelike-tutorial-03-scrolling-through.html
from dataclasses import dataclass
import numpy as np
from tcod import random

@dataclass
class WorldBuilder:
    width: int
    height: int
    tiles: np.zeros(shape=(width,height),order='F')

    def randomize_tiles(self):
        for x in range(len(self.width)):
            for y in range(len(self.height)):
                if random.Random().uniform(low=0.0,high=1.0) < 0.5:
                    self.tiles[x][y] = 1
                else:
                    self.tiles[x][y] = 0
        return self.tiles

    def smooth_caves(self, times: int = 8):
        pass

    def build(self):
        pass

    def cave_cellular_automata(self):
        pass
