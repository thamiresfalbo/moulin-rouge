from attrs import define as component
import esper
from tcod.console import Console
import tcod.event
import numpy as np
from numpy.typing import NDArray
import constants
from typing import Any


# COMPONENTS
@component
class CRender:
    x: int
    y: int
    char: str
    fg: tuple
    bg: tuple


@component
class CMovement:
    x: int = 0
    y: int = 0


@component
class CMap:
    tiles: NDArray[np.uint8]


# PROCESSORS
class PRender(esper.Processor):
    """Renders anything. Please set priority higher than PMapRender."""

    def process(self, console):
        for ent, rend in self.world.get_component(CRender):
            console.print(rend.x, rend.y, rend.char, rend.fg, rend.bg)


class PMapRender(esper.Processor):
    """
    Renders the map.
    """

    def process(self, console):
        for ent, cmap in self.world.get_component(CMap):
            for y in range(len(cmap.tiles)):
                for x in range(len(cmap.tiles[0])):
                    if cmap.tiles[y, x] == True:
                        # console.print(
                        #     x, y, chr(0x20), constants.PURPLE, constants.BLACK
                        # )
                        pass
                    else:
                        console.print(
                            x, y, chr(0x2588), constants.PURPLE, constants.BLACK
                        )

    def is_walkable(self, x: int, y: int) -> bool:
        pass


class PMovement(esper.Processor):
    def process(self, console):
        for ent, (rend, mov) in self.world.get_components(CRender, CMovement):
            for event in tcod.event.wait():
                match event:
                    case tcod.event.Quit():
                        raise SystemExit()
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                        mov.x -= 1
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                        mov.x += 1
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                        mov.y -= 1
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                        mov.y += 1
            # TODO Make player not move if the destination tile is not walkable.
            # if not self.world.get_processor(PMapRender).is_walkable(mov.x,mov.y):
            #     return
            rend.x = mov.x
            rend.y = mov.y
