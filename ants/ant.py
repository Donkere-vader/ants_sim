from random import random


class Ant:
    def __init__(self, pos):
        self.pos = pos
        self.moving = [1, 1]

    def move_to(self, pos):
        pass

    def update(self, delta_time):
        # calculate movement
        # TODO

        for i in range(2):
            self.moving[i] += random() - 0.5

        for i in range(2):
            self.pos[i] += self.moving[i] * delta_time
