import tcod
from player import Player
import constants
from world.cellularautomata import CellularAutomata


# TODO: Add sdl window so that it can use layers.
def main() -> None:
    TILESET = tcod.tileset.load_tilesheet(
        "./assets/taffer8x8.png",
        columns=16,
        rows=16,
        charmap=tcod.tileset.CHARMAP_CP437,
    )

    console = tcod.console.Console(constants.WIDTH, constants.HEIGHT, order="F")
    console.rgb["bg"] = constants.BLACK
    console.rgb["fg"] = constants.WHITE
    player = Player(constants.WIDTH // 2, constants.HEIGHT // 2)

    def create_world():
        w = CellularAutomata(height=constants.HEIGHT, width=constants.WIDTH).build()
        for y in range(constants.HEIGHT):
            for x in range(constants.WIDTH):
                # TODO: Use console.tiles_rgb instead
                if w[y, x]:
                    console.print(x, y, string=chr(0x20), fg=constants.WHITE)
                else:
                    console.print(x, y, string=chr(0x2588), fg=constants.WHITE)

    create_world()
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
                elif isinstance(event, tcod.event.KeyDown):
                    if event.sym == tcod.event.KeySym.SPACE:
                        create_world()
                elif isinstance(event, tcod.event.MouseMotion):
                    continue


if __name__ == "__main__":
    main()
