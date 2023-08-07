import tcod
import esper
import director
import constants
from map_builder import MCellularAutomata

# import pygame


# TODO Make it data-driven
# TODO Implement graphical window
# TODO Find a graphical tileset?
def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        "./assets/taffer9x9.png",
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    root_console = tcod.console.Console(constants.WIDTH, constants.HEIGHT, "F")
    my_map = MCellularAutomata(constants.WIDTH, constants.HEIGHT).make_caves().build()

    world = esper.World()

    e_player = world.create_entity()
    e_map = world.create_entity(director.CMap(my_map))
    world.add_component(
        e_player,
        director.CRender(
            len(my_map[0]) // 2,
            len(my_map) // 2,
            "@",
            constants.YELLOW,
            constants.BLACK,
        ),
    )

    world.add_component(e_player, director.CMovement())
    world.add_processor(director.PMapRender(), priority=1)
    world.add_processor(director.PMovement())

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
