from random import randint, random


def get_random_pos(bounds: tuple) -> tuple:
    return (randint(0, bounds[0]), randint(0, bounds[1]))


def pos_close_to(pos: tuple, distance = 10) -> tuple:
    return (pos[0] + random() * distance, pos[1] + random() * distance)
