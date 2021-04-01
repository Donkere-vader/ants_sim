import pygame
from pygame.locals import *
from .ant import Ant
from .config import *
from .functions import get_random_pos, pos_close_to, get_chunk, distance_to


# pygame setup
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()


class Game:
    def __init__(self):
        self.screen_width, self.screen_height = SCREEN_HEIGHT, SCREEN_WIDTH
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.setup()


        self.run = True
        self.game_loop()
    
    def setup(self):
        """ Setup the game variables """
        self.ticks: int = 0
        self.chunks: list[list[list[Object]]] = [[[] for _ in range(CHUNKS[0])] for _ in range(CHUNKS[1])]

        # objects
        self.home: list = [self.screen_width // 2, self.screen_height // 2]
        self.ants: list[Ant] = [Ant(self.home.copy()) for _ in range(N_ANTS)]

        for ant in self.ants:
            self.place_in_chunk(ant)

        # [[[position_x, position_y], life_time_left], more items...]
        self.home_trace: list[list[list[float, float], float]] = []
        self.food_trace: list[list[list[float, float], float]] = []

        # create food
        self.food: list[list[int, int]] = []
        for _ in range(N_FOOD_SPOTS):
            food_blob_pos = get_random_pos((self.screen_width, self.screen_height))
            for _ in range(N_FOOD_PER_SPOT):
                food = pos_close_to(food_blob_pos)
                food = [max(1, min(SCREEN_WIDTH-1, food[0])), max(1, min(SCREEN_HEIGHT-1, food[1]))]
                self.food.append(food)
                self.place_in_chunk(food)

    def game_loop(self):
        while self.run:
            self.screen.fill((0, 0, 0))

            self.update(1000 / fps / 1000)
            self.draw()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            pygame.display.flip()
            fpsClock.tick(fps)
    

    
    def place_in_chunk(self, obj, pos=None):
        if pos is None:
            pos = obj
            if hasattr(obj, 'pos'):
                pos = obj.pos

        chunk_pos = get_chunk(pos)
        self.chunks[chunk_pos[1]][chunk_pos[0]].append(obj)

        if hasattr(obj, 'chunk_pos'):
            obj.chunk_pos = chunk_pos

    def remove_from_chunk(self, obj, chunk_pos=None):
        if chunk_pos is None:
            chunk_pos = obj
            if hasattr(obj, 'chunk_pos'):
                chunk_pos = obj.chunk_pos

        if obj in self.chunks[chunk_pos[1]][chunk_pos[0]]:
            self.chunks[chunk_pos[1]][chunk_pos[0]].remove(obj)

    def update(self, delta_time):
        self.ticks += 1
        for ant in self.ants:
            ant.update(delta_time)
            
            # update chunk
            if self.ticks % 2 == 0:
                self.remove_from_chunk(ant)
                self.place_in_chunk(ant)

            # check objects
            objs = self.get_objects_around_chunk(ant.chunk_pos)

            weakest_food_trace = None
            weakest_home_trace = None

            for obj in objs:
                if type(obj) == Ant:
                    continue

                if not ant.has_food:
                    if type(obj[0]) == float:  # food
                        if distance_to(obj, ant.pos) > ANT_VISION:
                            continue

                        if distance_to(obj, ant.pos) < 8:
                            ant.has_food = True
                            self.food.remove(obj)
                            self.remove_from_chunk(obj, chunk_pos=get_chunk(obj))
                        else:
                            ant.move_to(obj)
                            break

                    if type(obj[0]) == list and obj[2] == 'food':  # food trace
                        if distance_to(obj[0], ant.pos) > ANT_VISION:
                            continue

                        if weakest_food_trace is None or weakest_food_trace[1] > obj[1]:
                            weakest_food_trace = obj
                else:
                    if type(obj[0]) == list and obj[2] == 'home':  # food trace
                        if distance_to(obj[0], ant.pos) > ANT_VISION:
                            continue

                        if weakest_home_trace is None or weakest_home_trace[1] > obj[1]:
                            weakest_home_trace = obj

                    if distance_to(ant.pos, self.home) < 8:
                        ant.has_food = False
                
            if ant.has_food and weakest_home_trace is not None:
                ant.move_to(weakest_home_trace[0])
            elif weakest_food_trace is not None:
                ant.move_to(weakest_food_trace[0])

            # place trace
            if self.ticks % 10 == 0:
                trace = [
                    ant.pos.copy(),
                    1,
                    'food' if ant.has_food else 'home',
                ]
                if not ant.has_food:
                    self.home_trace.append(trace)
                else:
                    self.food_trace.append(trace)
                self.place_in_chunk(trace, pos=trace[0])

        for lst in [self.home_trace, self.food_trace] :
            for trace in lst:
                trace[1] -= 0.0001

                if trace[1] < 0:
                    lst.remove(trace)
                    self.remove_from_chunk(trace, chunk_pos=get_chunk(obj[0]))

    def get_objects_around_chunk(self, chunk_pos) -> list:
        objects = []

        for y in range(-1, 2):
            y = chunk_pos[1] + y
            for x in range(-1, 2):
                x = chunk_pos[0] + x

                if not CHUNKS[0] > x >= 0 or not CHUNKS[1] > y >= 0:
                    continue

                objects += self.chunks[y][x]

        return objects

    def draw(self):
        """ Draw all the simulation items on screen """

        # draw home
        pygame.draw.circle(self.screen, (0, 0, 255), self.home, 10)

        # draw traces
        for lst, color in zip([self.home_trace, self.food_trace], [[0, 0, 255], [255, 255, 255]]):
            for trace in lst:
                c = color.copy()
                for i in range(3):
                    c[i] = c[i] * trace[1]
                pygame.draw.circle(self.screen, c, trace[0], 1)

        # draw ants
        for ant in self.ants:
            pygame.draw.circle(self.screen, (255, 0, 0), ant.pos, 3)

        # draw food
        for food in self.food:
            pygame.draw.circle(self.screen, (0, 255, 0), food, 1)
