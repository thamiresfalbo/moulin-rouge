import esper
from tcod.console import Console
import tcod.event
from attrs import define as component
from attrs import field
from numpy.typing import NDArray
from typing import Any
import constants


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
    x: int = field(init=False)
    y: int = field(init=False)


@component
class CMap:
    tiles: NDArray[Any]


@component
class CLog:
    x: int = field(init=False, default=0)
    y: int = field(init=False, default=constants.HEIGHT - 10)
    width: int = field(init=False, default=constants.WIDTH)
    height: int = field(init=False, default=10)


# PROCESSORS
class PMapRender(esper.Processor):
    """Renders the map view."""

    # Theory: https://roguebasin.com/index.php/Scrolling_map
    def process(self, console: Console):
        for ent, cmap in self.world.get_component(CMap):
            camera = self.camera_pos(console, cmap)
            for x in range(constants.MAP_VIEW_WIDTH):
                for y in range(constants.MAP_VIEW_HEIGHT):
                    console.rgb[x, y] = cmap.tiles[x + camera[0], y + camera[1]]["dark"]

        for ent, rend in self.world.get_component(CRender):
            console.print(
                rend.x - camera[0], rend.y - camera[1], rend.char, rend.fg, rend.bg
            )

    def camera_pos(self, console: Console, cmap: CMap) -> tuple:
        """Calculates camera position from the map coordinates."""

        for ent, rend in self.world.get_component(CRender):
            half_x = int(constants.MAP_VIEW_WIDTH / 2)
            half_y = int(constants.MAP_VIEW_HEIGHT / 2)
            camera_x = rend.x - half_x
            camera_y = rend.y - half_y

            if rend.x < half_x:
                camera_x = 0
            elif rend.x > len(cmap.tiles[0]) - half_x:
                camera_x = len(cmap.tiles[0]) - constants.MAP_VIEW_WIDTH

            if rend.y < half_y:
                camera_y = 0
            elif rend.y > len(cmap.tiles) - half_y:
                camera_y = len(cmap.tiles) - constants.MAP_VIEW_HEIGHT

        return (camera_x, camera_y)


class PLogRender(esper.Processor):
    """Renders the log window."""

    def process(self, console: Console):
        for ent, clog in self.world.get_component(CLog):
            console.draw_frame(
                x=clog.x,
                y=clog.y,
                width=clog.width,
                height=clog.height,
                title="Log",
            )


class PMovement(esper.Processor):
    """Processes player keys."""

    def process(self, console):
        for ent, (rend, mov) in self.world.get_components(CRender, CMovement):
            mov.x = rend.x
            mov.y = rend.y
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

            # Checks if player can walk in the tile.
            for ent, cmap in self.world.get_component(CMap):
                if not cmap.tiles[mov.x, mov.y]["walkable"]:
                    return
                else:
                    rend.x = mov.x
                    rend.y = mov.y
