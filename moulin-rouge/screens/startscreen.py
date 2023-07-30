import tcod
import sys
sys.path.append("..")
import constants
from player import Player
import worldbuilder
import numpy as np
def start_screen():
    TILESET = tcod.tileset.load_tilesheet('./assets/tileset.png',
                                            columns=16,
                                            rows=16,
                                            charmap=tcod.tileset.CHARMAP_CP437)

    console = tcod.console.Console(constants.WIDTH,constants.HEIGHT, order='F')
    console.rgb['bg'] = constants.BLACK
    console.rgb['fg'] = constants.WHITE
    player = Player(constants.WIDTH//2,constants.HEIGHT//2)

    def create_world():
        w = worldbuilder.CaveGenerator(constants.WIDTH, constants.HEIGHT)
        w.randomize_tiles()
        w.smooth_caves()
        w.build()

    with tcod.context.new(columns=constants.WIDTH,rows=constants.HEIGHT,tileset=TILESET) as context:
        while True:
            console.clear()
            player.on_draw(console)
            context.present(console)
            for event in tcod.event.wait():
                print(event)
                player.on_event(event)

