import tcod
import constants


def main() -> None:
    width = 80
    height = 50
    tileset = tcod.tileset.load_tilesheet('./assets/taffer8x8.png',columns=16,rows=16,charmap=tcod.tileset.CHARMAP_CP437)
    console = tcod.console.Console(width,height, order='F')
    console.rgb['bg'] = constants.BLACK
    console.rgb['fg'] = constants.WHITE
    # console.rgb['ch'] =
    console.print(0,0,'Hello, World.')
    with tcod.context.new(columns=console.width,rows=console.height,tileset=tileset) as context:
        while True:
            context.present(console)
            for event in tcod.event.wait():
                print(event)
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()

if __name__ == "__main__":
    main()
