import tcod
from cartographer import RandomWalk
import director
import constants
import esper


# TODO Add sdl window for layers.
def main() -> None:
    tileset = "assets/taffer8x8.png"
    TILESET = tcod.tileset.load_tilesheet(
        tileset,
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    console = tcod.console.Console(constants.WIDTH, constants.HEIGHT, order="F")
    console.rgb["bg"] = constants.BLACK
    console.rgb["fg"] = constants.WHITE

    w = esper.World()
    player = w.create_entity(
        director.CRender(0, 0, "@", constants.YELLOW, constants.BLACK),
        director.CMovement(0, 0),
    )

    render_processor = director.PRender(console)
    w.add_processor(render_processor)

    with tcod.context.new(
        columns=constants.WIDTH,
        rows=constants.HEIGHT,
        tileset=TILESET,
        title="Moulin Rouge",
    ) as context:
        while True:
            context.present(console)
            for event in tcod.event.wait():
                print(event)
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
            w.process()


if __name__ == "__main__":
    main()
