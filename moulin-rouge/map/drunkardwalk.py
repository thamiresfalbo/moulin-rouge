import numpy as np
from map.map_architect import MapArchitect
from numpy.typing import NDArray
import copy


class DrunkWalkWalk(MapArchitect):
    """A map made by drunk dwarves."""

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.tiles: NDArray[np.uint8] = np.zeros((self.height, self.width))

    def build(self):
        PASS_OUT = 400
        total_tiles = np.count_nonzero(self.tiles)
        amount_needed = int(self.tiles.size * 0.45)

        # TODO Check out of bounds
        center = [int(self.height / 2), int(self.width / 2)]
        self.tiles[center[0], center[1]] = 1
        for i in range(5):
            drunk_y = copy.copy(center[0])
            drunk_x = copy.copy(center[1])
            for _ in range(PASS_OUT):
                r = np.random.randint(5)
                if r == 4:
                    drunk_x += 1
                elif r == 3:
                    drunk_x -= 1
                elif r == 2:
                    drunk_y += 1
                elif r == 1:
                    drunk_y -= 1

                if self.__out_of_bounds(drunk_x, drunk_y):
                    drunk_x = 0
                    drunk_y = 0
                self.tiles[drunk_y, drunk_x] = 1

        return self.tiles

    def __out_of_bounds(self, x: int, y: int):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return False
