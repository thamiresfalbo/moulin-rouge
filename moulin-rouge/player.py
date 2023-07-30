import tcod
import constants
from attrs import define as component

@component
class Player:
    x: int
    y: int
    _color: tuple = constants.YELLOW

    def on_draw(self, console: tcod.console.Console) -> None:
        console.print(self.x, self.y, '@', self._color)#or use a chr(0x263B) for a happy face

    def on_event(self, event: tcod.event.Event) -> None:
        match event:
            case tcod.event.Quit():
                raise SystemExit()
            case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                self.x -= 1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                self.x += 1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                self.y -= 1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                self.y += 1
