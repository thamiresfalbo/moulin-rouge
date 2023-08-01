import tcod
from player import Player
import constants
from cartographer import RandomWalk
from director import Director


# TODO Add sdl window for layers.
def main() -> None:
    tileset = "./assets/taffer8x8.png"
    TILESET = tcod.tileset.load_tilesheet(
        tileset,
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    console = tcod.console.Console(constants.WIDTH, constants.HEIGHT, order="F")
    console.rgb["bg"] = constants.BLACK
    console.rgb["fg"] = constants.WHITE
    player = Player(constants.WIDTH // 2, constants.HEIGHT // 2)
    # Wandavision?
    agnes = Director()

    def create_world():
        w = RandomWalk(constants.WIDTH, constants.HEIGHT).make_caves().build()
        for y in range(constants.HEIGHT):
            for x in range(constants.WIDTH):
                # TODO Use console.tiles_rgb instead
                if w[y, x] == 0:
                    # Walls
                    console.print(x, y, string=chr(0x2593), fg=constants.WHITE)
                elif w[y, x] == 1:
                    # Floors
                    console.print(x, y, string=chr(0x20), fg=constants.WHITE)

    create_world()
    with tcod.context.new(
        columns=constants.WIDTH,
        rows=constants.HEIGHT,
        tileset=TILESET,
        title="Moulin Rouge",
    ) as context:
        # TODO Add an director/engine
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
