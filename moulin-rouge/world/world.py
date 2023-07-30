'''
How it will work:
The map will be a 2d array with Boolean Values
'''
import numpy as np
from tcod import bsp,los
import random

class World():
    def __init__(self, width:int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles = np.empty(shape=[self.width,self.height],dtype=np.bool_ , order='F')

    def build(self):
        return self.tiles
