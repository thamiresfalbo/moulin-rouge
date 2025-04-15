import tcod
import esper
import constants
from screens.start_screen import start_screen
from screens.main_menu import main_menu
import libs.terminal as terminal


# TODO Make it data-driven
# TODO Add Graphics
def main() -> None:
    # terminal.open()
    # terminal.printf(1, 1, "Hello, world!")
    # terminal.refresh()

    # while terminal.read() != terminal.TK_CLOSE:
    #     pass

    # terminal.close()
    tileset = tcod.tileset.load_tilesheet(
        "./assets/simple-mood-boxy16x16.png",
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    root_console = tcod.console.Console(constants.WIDTH, constants.HEIGHT, "F")

    world = esper.World()
    main_menu(world)

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


if __name__ == "__main__":
    main()
