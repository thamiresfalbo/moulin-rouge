from attrs import define, field
import esper
from tcod.console import Console
import tcod.event
import map_builder
import numpy as np
from numpy.typing import NDArray
import constants


# COMPONENTS
@define
class CRender:
    x: int
    y: int
    char: str
    fg: tuple
    bg: tuple


@define
class CMovement:
    x: int = 0
    y: int = 0


# TODO Finish CMap component
@define
class CMap:
    tiles: NDArray[np.uint8]


# PROCESSORS
class PRender(esper.Processor):
    def process(self, console):
        console.clear()
        for ent, rend in self.world.get_component(CRender):
            console.print(rend.x, rend.y, rend.char, rend.fg, rend.bg)


# TODO Apply cartographer to PMapRender
class PMapRender(esper.Processor):
    def process(self, console):
        for ent, (rend, cmap) in self.world.get_components(CRender, CMap):
            for y in cmap.tiles:
                for x in cmap.tiles[y]:
                    if cmap.tiles[y, x] == 1:
                        console.print(x, y, " ", constants.WHITE, constants.BLACK)
                    else:
                        console.print(x, y, "#", constants.WHITE, constants.BLACK)

    def is_walkable(self, x: int, y: int) -> None:
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
