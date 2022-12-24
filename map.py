import pygame as pg
from settings import *
import random

_ = False
d = 'd'

mini_map = [
    [1, 1, 1, 1, 1, 1, 1, d, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [d, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, d],
    [1, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, d, 1, 1, 1, 1, 1, 1, 1, 1],
]

maps_dict = {
    1: [
    [1, 1, 1, 1, 1, 1, 1, d, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [d, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, d],
    [1, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, d, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    2: [
    [1, 1, 1, 1, 1, 1, 1, d, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, 2, 2, 2, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, 1],
    [d, _, _, _, _, _, 2, _, _, _, _, _, 2, _, _, d],
    [1, _, _, 2, _, 2, 2, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, 2, 2, _, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, 2, _, _, _, 2, _, _, _, 2, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, d, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    3: [
    [1, 1, 1, 1, 1, 1, 1, d, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, _, _, _, _, _, 3, 3, 3, _, _, 1],
    [1, _, _, _, _, _, 3, _, _, _, _, _, 3, _, _, 1],
    [d, _, _, _, _, _, 3, _, _, _, _, _, 3, _, _, d],
    [1, _, _, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, _, _, 1],
    [1, _, _, _, _, _, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 3, _, _, _, 3, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, d, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
}

floor_map = [[0 for __ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]


class Map:
    def __init__(self, game):
        self.game = game
        self.generate_floor()
        # self.mini_map = mini_map
        self.load_new_room() #loads room where player starts
        self.world_map = {}
        self.get_map()
    
    def get_neighbors(self):
        grid_height = len(self.floor_map)
        grid_width = len(self.floor_map[1])
        res = {}
        for x in range(grid_height):
            for y in range(grid_width):
                res[(y, x)] = set()
                if self.floor_map[(x - 1) % grid_height][y]:
                    res[(y, x)].add((y, (x - 1) % grid_height))
                if self.floor_map[x][(y - 1) % grid_width]:
                    res[(y, x)].add(((y - 1)  % grid_width, x))
                if self.floor_map[(x + 1) % grid_height][y]:
                    res[(y, x)].add((y, (x + 1) % grid_height))
                if self.floor_map[x][(y + 1) % grid_width]:
                    res[(y, x)].add(((y + 1) % grid_width, x))

        self.neighbors = res

    def shut_unused_doors(self):
        grid_height = len(self.floor_map)
        grid_width = len(self.floor_map[1])

        for x in range(grid_height):
            for y in range(grid_width):
                if self.floor_map[x][y]:
                    if (y , (x - 1) % grid_height) not in self.neighbors[(y, x)]:
                        for i in range(len(self.room_dict[(y, x)][0])):
                            self.room_dict[(y, x)][0][i] = 1
                    if ((y - 1) % grid_width, x) not in self.neighbors[(y, x)]:
                        for i in range(len(self.room_dict[(y, x)])):
                            self.room_dict[(y, x)][i][0] = 1
                    if (y , (x + 1) % grid_height) not in self.neighbors[(y, x)]:
                        for i in range(len(self.room_dict[(y, x)][0])):
                            self.room_dict[(y, x)][-1][i] = 1
                    if ((y + 1) % grid_width, x) not in self.neighbors[(y, x)]:
                        for i in range(len(self.room_dict[(y, x)])):
                            self.room_dict[(y, x)][i][-1] = 1


    def check_connectivity(self, node):
        queue = []

        self.visited.add(node)
        queue.append(node)

        while queue:
            m = queue.pop(0)
            for nei in self.neighbors[m]:
                if nei not in self.visited:
                    self.visited.add(nei)
                    queue.append(nei)

    def load_new_room(self):
        x, y = self.game.player.floor_x, self.game.player.floor_y
        self.mini_map = self.room_dict[(y, x)]

    def randomize_floor_layout(self):
        # self.floor_map = [
        #     [0, 0, 0, 1, 1, 0, 1],
        #     [1, 1, 1, 1, 0, 1, 1],
        #     [0, 1, 0, 1, 1, 1, 1],
        #     [0, 0, 0, 0, 1, 0, 1],
        #     [0, 1, 1, 1, 1, 0, 0],
        #     [0, 1, 0, 1, 1, 0, 0],
        #     [0, 1, 1, 0, 1, 0, 0],
        #     [0, 1, 0, 0, 1, 0, 0],
        #     [0, 1, 1, 1, 1, 1, 1],
        # ]
        # self.room_number = 13

        self.floor_map = [[0 for __ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self.floor_map[self.game.player.floor_x][self.game.player.floor_y] = 1
        for _ in range(self.room_number - 1):
            x, y = random.randint(0, MAP_HEIGHT - 1), random.randint(0, MAP_WIDTH - 1)
            self.floor_map[x][y] = random.randint(1, 3)

        pass #+1 for each room generated

    def generate_floor(self):
        self.visited = set()
        self.room_number = random.randint(int(2*(MAP_HEIGHT + MAP_WIDTH)), MAP_HEIGHT * MAP_WIDTH)
        
        self.room_dict = {}

        while len(self.visited) < self.room_number // 2:
            self.randomize_floor_layout()
            self.visited = set()
            neighbors = self.get_neighbors()
            self.check_connectivity((PLAYER_POS_FLOOR)[::-1])
        
        for x in range(MAP_HEIGHT):
            for y in range(MAP_WIDTH):
                if self.floor_map[x][y]:
                    self.room_dict[(y, x)] = maps_dict[self.floor_map[x][y]].copy() # self.room_type[self.floor_map[x][y]].copy()
        
        # self.shut_unused_doors()
    
    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value
    
    def draw(self):
        [pg.draw.rect(self.game.screen, "darkgray", (pos[0] * 100, pos[1] * 100, 100, 100), 2)
        for pos in self.world_map]