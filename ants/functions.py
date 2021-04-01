from random import randint, random
from .config import CHUNK_WIDTH, CHUNK_HEIGHT
from math import sqrt, atan


def get_random_pos(bounds: tuple) -> list:
    return [randint(0, bounds[0]), randint(0, bounds[1])]


def pos_close_to(pos: tuple, distance = 30) -> list:
    return [pos[0] + random() * distance, pos[1] + random() * distance]


def get_chunk(pos) -> list:
    return [int(pos[0] // CHUNK_WIDTH), int(pos[1] // CHUNK_HEIGHT)]


def distance_to(pos, pos2) -> float:
    return sqrt(abs(pos[0] - pos2[0])**2 + abs(pos[1] - pos2[1])**2)


def angle_to(pos, pos2) -> float:
    delta_x = pos2[0] - pos[0]
    delta_y = pos2[1] - pos[1]
    return atan(delta_y / delta_x)
