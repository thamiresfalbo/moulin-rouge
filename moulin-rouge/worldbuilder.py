# Inspired by this tutorial(in Java):
# http://trystans.blogspot.com/2011/08/roguelike-tutorial-03-scrolling-through.html
# https://roguebasin.com/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
# TODO: Refactor this file

import numpy as np
from tcod import random
import tiles


class World:
    def __init__(self, width:int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles = np.ndarray(shape=[self.width,self.height], order='F')

class CaveGenerator:
    def __init__(self, width:int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles = np.ndarray(shape=[self.width,self.height], order='F')

    def randomize_tiles(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                if random.Random().uniform(low=0.0,high=1.0) < 0.5:
                    self.tiles[x][y] = 0
                else:
                    self.tiles[x][y] = 1

    # Check the neighbour tiles(3x3). A tile becomes a wall if there are 5 walls in the region.
    def smooth_caves(self, times: int = 8) -> None:
        tiles2 = np.ndarray(shape=[self.width,self.height], order='F')
        for time in range(times):
            for x in range(self.width):
                for y in range(self.height):
                    floors = 0
                    rocks = 0

        self.tiles = np.copy(tiles2)

    # Used to connect isolated caves.
    def flood_fill(self):
        pass

    def build(self):
        return self.tiles

class RogueDungeon:
    pass

class DrunkWalkDungeon:
    pass
