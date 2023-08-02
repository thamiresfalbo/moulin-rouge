import tcod
import director
import constants
import esper


# TODO Add sdl window for layers.
def main() -> None:
    tileset = "assets/tileset.png"
    TILESET = tcod.tileset.load_tilesheet(
        tileset,
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    # Wandavision?
    agnes = esper.World()
    player = agnes.create_entity()
    agnes.add_component(
        player,
        director.CRender(
            constants.CENTER[0],
            constants.CENTER[1],
            "@",
            constants.YELLOW,
            constants.BLACK,
        ),
    )
    agnes.add_component(
        player,
        director.CMovement(constants.CENTER[0], constants.CENTER[1]),
    )

    root_console = tcod.console.Console(constants.WIDTH, constants.HEIGHT)
    render_processor = director.PRender()
    movement_processor = director.PMovement()
    agnes.add_processor(render_processor)
    agnes.add_processor(movement_processor)

    with tcod.context.new(
        columns=constants.WIDTH,
        rows=constants.HEIGHT,
        tileset=TILESET,
        title="Moulin Rouge",
        vsync=True,
    ) as context:
        while True:
            context.present(root_console)
            agnes.process(root_console)


if __name__ == "__main__":
    main()
