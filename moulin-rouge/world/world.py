"""
How it will work:
The map will be a 2d array with Boolean Values
Walls are false values.
Floors are true values.
"""
import numpy as np
from numpy.typing import NDArray


class World:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles: NDArray[np.bool_] = np.zeros(
            shape=[self.width, self.height], dtype=np.bool_
        )
