import tcod
import constants
import player

#TODO: Add sdl window so that it can use layers.
def main() -> None:
    TILESET = tcod.tileset.load_tilesheet('./assets/tileset.png',
                                          columns=16,
                                          rows=16,
                                          charmap=tcod.tileset.CHARMAP_CP437)
    console = tcod.console.Console(constants.WIDTH,constants.HEIGHT, order='F')
    console.rgb['bg'] = constants.COLORS['BLACK']
    console.rgb['fg'] = constants.COLORS['WHITE']
    console.print(0,0,'Hello, World.')
    p = player.Player(constants.WIDTH//2,constants.HEIGHT//2)
    with tcod.context.new(columns=console.width,rows=console.height,tileset=TILESET) as context:
        while True:
            console.clear()
            p.on_draw(console)
            context.present(console)
            for event in tcod.event.wait():
                print(event)
                p.on_event(event)

if __name__ == "__main__":
    main()
