import esper
from tcod.console import Console
import tcod.event
import constants
from attrs import define as component
import numpy as np
from numpy.typing import NDArray

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


@component
class CCamera:
    width: int
    height: int


# PROCESSORS
class PRender(esper.Processor):
    def process(self, console: Console):
        for ent, rend in self.world.get_component(CRender):
            console.print(rend.x, rend.y, rend.char, rend.fg, rend.bg)


class PMapRender(esper.Processor):
    def process(self, console: Console):
        for ent, cmap in self.world.get_component(CMap):
                for ent, rend in self.world.get_component(CRender):
                    for y in range(console.height):
                        for x in range(console.width):
                            cur_x = x - int(console.width/2)
                            cur_y = y - int(console.height/2)
                            if cmap.tiles[y + cur_y,x + cur_x] == False:
                                console.print(
                                    x,
                                    y,
                                    '#',
                                    constants.WHITE,
                                    constants.BLACK,
                                )
                            else:
                                console.print(
                                    x,
                                    y,
                                    '.',
                                    constants.WHITE,
                                    constants.BLACK,
                                )

    def check_pos(self, x:int, y:int, console: Console) -> list:
        pass



    def is_walkable(self, x: int, y: int) -> bool:
        pass


class PCamera(esper.Processor):
    def process(self, console):
        pass

# TODO Make player not move if the destination tile is not walkable.
# TODO Finish implementing the scrolling map
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

            rend.x = mov.x
            rend.y = mov.y
            # if not self.world.get_processor(PMapRender).is_walkable(mov.x,mov.y):
            #     return
