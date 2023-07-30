import tcod
from player import Player
import constants
from world.cellularautomata import CellularAutomata

#TODO: Add sdl window so that it can use layers.
def main() -> None:
    TILESET = tcod.tileset.load_tilesheet('./assets/taffer8x8.png',
                                            columns=16,
                                            rows=16,
                                            charmap=tcod.tileset.CHARMAP_CP437)

    console = tcod.console.Console(constants.WIDTH,constants.HEIGHT, order='F')
    console.rgb['bg'] = constants.BLACK
    console.rgb['fg'] = constants.WHITE
    player = Player(constants.WIDTH//2,constants.HEIGHT//2)

    def create_world():
        w = CellularAutomata(constants.WIDTH,constants.HEIGHT).make_caves().build()
        for x in range(constants.WIDTH):
            for y in range(constants.HEIGHT):
                #TODO: Use console.tiles_rgb instead
                if w[x][y] == 0:
                    console.print(x,y,string=chr(0x2588),fg=constants.WHITE) # Wall
                elif w[x][y] == 1:
                    console.print(x,y,string=chr(0x20),fg=constants.WHITE) # Floor

    #TODO: Make it not generate a new map when inside context loop.
    create_world()

    with tcod.context.new(columns=constants.WIDTH,
                          rows=constants.HEIGHT,
                          tileset=TILESET,
                          title='Moulin Rouge'
                          ) as context:
        while True:
            # console.clear()

            context.present(console)
            for event in tcod.event.wait():
                print(event)
                if isinstance(event,tcod.event.Quit):
                    raise SystemExit()

if __name__ == "__main__":
    main()
