import tcod
import director
import constants
import esper
from map_builder import MCellularAutomata


# TODO Add sdl window for layers.
def main() -> None:
    tileset = "./assets/simple_mood16x16.png"
    TILESET = tcod.tileset.load_tilesheet(
        tileset,
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )
    root_console = tcod.console.Console(constants.WIDTH, constants.HEIGHT)

    my_map = MCellularAutomata(constants.WIDTH,constants.HEIGHT).make_caves().build()

    # ECS
    world = esper.World()

    # Entities
    e_player = world.create_entity()
    e_map = world.create_entity(director.CMap(my_map))

    # Processors
    world.add_processor(director.PMapRender(),priority=1)
    world.add_processor(director.PRender())
    world.add_processor(director.PMovement())
    world.add_processor(director.PCamera())

    # Components
    world.add_component(
        e_player,
        director.CRender(
            constants.CENTER[0],
            constants.CENTER[1],
            "@",
            constants.YELLOW,
            constants.BLACK,
        ),
    )
    world.add_component(
        e_player,
        director.CMovement(constants.CENTER[0], constants.CENTER[1]),
    )

    world.add_component(
        e_player, director.CCamera(root_console.width, root_console.height)
    )

    with tcod.context.new(
        columns=root_console.width,
        rows=root_console.height,
        tileset=TILESET,
        title="Moulin Rouge",
        vsync=True,
    ) as context:
        while True:
            context.present(root_console)
            root_console.clear()
            world.process(root_console)


if __name__ == "__main__":
    main()
