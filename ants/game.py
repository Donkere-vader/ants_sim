import pygame
from pygame.locals import *
from .ant import Ant
from .config import N_ANTS, N_FOOD
from .functions import get_random_pos, pos_close_to


# pygame setup
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()


class Game:
    def __init__(self):
        self.screen_width, self.screen_height = 640, 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.setup()

        self.run = True
        self.game_loop()
    
    def setup(self):
        self.home: tuple = (self.screen_width // 2, self.screen_height // 2)
        self.ants: list[Ant] = [Ant(self.home) for _ in range(N_ANTS)]

        food_blob_pos = get_random_pos((self.screen_width, self.screen_height))
        self.food: list[tuple] = [pos_close_to(food_blob_pos) for _ in range(N_FOOD)]

    def game_loop(self):
        while self.run:
            self.screen.fill((0, 0, 0))

            self.update(1000 / fps)
            self.draw()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            pygame.display.flip()
            fpsClock.tick(fps)


    def update(self, delta_time):
        pass

    def draw(self):
        """ Draw all the simulation items on screen """

        # draw ants
        for ant in self.ants:
            pygame.draw.circle(self.screen, (255, 0, 0), ant.pos, 3)

        # draw food
        for food in self.food:
            pygame.draw.circle(self.screen, (0, 255, 0), food, 1)
