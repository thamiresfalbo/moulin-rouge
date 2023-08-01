import numpy as np
from numpy.typing import NDArray


class MapArchitect:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles: NDArray[np.uint8]
