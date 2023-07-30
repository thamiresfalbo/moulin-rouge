import esper
import tcod
import constants
import attrs

@attrs.define(eq=False)
class Player:
    x: int
    y: int
    color: tuple = constants.COLORS['YELLOW']

    def on_draw(self, console: tcod.console.Console) -> None:
        console.print(self.x, self.y, '@', self.color)#or use a chr(0x263B) for a happy face

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

