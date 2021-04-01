from random import random
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, ANT_SPEED
from .functions import angle_to
import math


class Ant:
    def __init__(self, pos):
        self.pos = pos
        self.has_food = False
        self.chunk_pos = [0,  0]
        self.direction = random() * 2 * math.pi

    def move_to(self, pos):
        self.direction = angle_to(self.pos, pos)
        if pos[0] < self.pos[0]:
            self.direction += math.pi

    def update(self, delta_time):
        self.direction += (random() - .5) * 0.1

        # calculate movement
        self.pos[0] += math.cos(self.direction) * delta_time * ANT_SPEED
        self.pos[1] += math.sin(self.direction) * delta_time * ANT_SPEED

        if not SCREEN_WIDTH > self.pos[0] > 0 or not SCREEN_HEIGHT > self.pos[1] > 0:
            self.pos[0] -= math.cos(self.direction) * delta_time * ANT_SPEED
            self.pos[1] -= math.sin(self.direction) * delta_time * ANT_SPEED
            self.move_to((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
