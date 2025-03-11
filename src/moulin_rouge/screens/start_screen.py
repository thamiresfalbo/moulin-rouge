import constants
from map_builder import MRandomWalk
import esper
import director


def start_screen(world: esper.World):
    my_map = MRandomWalk(100, 100).make_caves().build()
    e_player = world.create_entity(
        director.CRender(
            len(my_map[0]) // 2,
            len(my_map) // 2,
            "@",
            constants.YELLOW,
            constants.BLACK,
        ),
        director.CMovement(),
    )
    e_map = world.create_entity(director.CMap(my_map))
    e_log = world.create_entity(director.CLog())

    world.add_processor(director.PLogRender())
    world.add_processor(director.PMapRender(), priority=1)
    world.add_processor(director.PMovement())
    world.add_processor(director.PLogRender())
