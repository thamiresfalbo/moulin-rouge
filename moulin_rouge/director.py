from attrs import define as component
import esper
from tcod.console import Console
from tcod.context import Context
import tcod.event


# Components
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


# Processors
class PRender(esper.Processor):
    def __init__(self, console: Console) -> None:
        super().__init__()
        self.console = console

    def process(self):
        for ent, rend in self.world.get_component(CRender):
            self.console.print(rend.x, rend.y, rend.char, rend.fg, rend.bg)


# class PMovement(esper.Processor):
#     def process(self,event):
#         pass
