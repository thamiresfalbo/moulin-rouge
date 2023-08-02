import tcod
import director
import constants
import esper
from map_builder import MCellularAutomata


# TODO Add sdl window for layers.
def main() -> None:
    tileset = "assets/tileset.png"
    TILESET = tcod.tileset.load_tilesheet(
        tileset,
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )
    root_console = tcod.console.Console(constants.WIDTH, constants.HEIGHT)

    my_map = MCellularAutomata(constants.WIDTH, constants.HEIGHT).make_caves().build()
    world = esper.World()

    # Entities
    player = world.create_entity()
    entity_map = world.create_entity()

    # Processors
    world.add_processor(director.PRender())
    world.add_processor(director.PMapRender())
    world.add_processor(director.PMovement())

    # Components
    world.add_component(entity_map, director.CMap(my_map))
    world.add_component(
        player,
        director.CRender(
            constants.CENTER[0],
            constants.CENTER[1],
            "@",
            constants.YELLOW,
            constants.BLACK,
        ),
    )
    world.add_component(
        player,
        director.CMovement(constants.CENTER[0], constants.CENTER[1]),
    )

    with tcod.context.new(
        columns=constants.WIDTH,
        rows=constants.HEIGHT,
        tileset=TILESET,
        title="Moulin Rouge",
        vsync=True,
    ) as context:
        while True:
            context.present(root_console)
            world.process(root_console)


if __name__ == "__main__":
    main()
