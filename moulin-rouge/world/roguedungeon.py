from world.world import World
import numpy as np
from tcod import bsp,los
import random

class RogueDungeon(World):
    """A classic, simple room-based dungeon."""

    def makeCaves(self) -> np.ndarray:
        bsp = bsp.BSP(x=0,y=0,width=80,height=40)
        bsp.split_recursive(depth=5,
                          min_width=3,
                          min_height=3,
                          max_horizontal_ratio=1.5,
                          max_vertical_ratio=1.5
                          )

    def connect_caves(self):
        # los.bresenham
        pass
