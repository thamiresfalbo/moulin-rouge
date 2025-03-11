import tcod
import esper
import constants
from screens.start_screen import start_screen


# TODO Make it data-driven
def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        "./assets/simple-mood-boxy16x16.png",
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    root_console = tcod.console.Console(constants.WIDTH, constants.HEIGHT, "F")

    world = esper.World()
    start_screen(world)

    with tcod.context.new(
        columns=root_console.width,
        rows=root_console.height,
        tileset=tileset,
        title="Moulin Rouge",
        vsync=True,
    ) as context:
        while True:
            root_console.clear()
            world.process(root_console)
            context.present(root_console)


# if __name__ == "__main__":
#     main()
