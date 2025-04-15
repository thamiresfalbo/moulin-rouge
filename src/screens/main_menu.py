import constants
import tcod
import esper


def main_menu(world: esper.World):
    world.print(
        constants.WIDTH // 2,
        constants.HEIGHT // 2,
        "It takes a long way to walk around.",
    )
