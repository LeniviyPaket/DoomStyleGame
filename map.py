import pygame as pg
from settings import *
from random import randint

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
        self.floor_map = [
            [0, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 0, 0],
            [0, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 0],
        ]
        self.room_number = 13
        pass #+1 for each room generated

    def generate_floor(self):
        self.visited = set()
        self.room_number = randint(int(2.5*(MAP_HEIGHT + MAP_WIDTH)), MAP_HEIGHT * MAP_WIDTH)
        
        self.room_dict = {}

        while len(self.visited) < self.room_number // 2:
            self.randomize_floor_layout()
            self.visited = set()
            neighbors = self.get_neighbors()
            self.check_connectivity((PLAYER_POS_FLOOR)[::-1])
        
        for x in range(MAP_HEIGHT):
            for y in range(MAP_WIDTH):
                if self.floor_map[x][y]:
                    self.room_dict[(y, x)] = mini_map # self.room_type[self.floor_map[x][y]]
    
    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value
    
    def draw(self):
        [pg.draw.rect(self.game.screen, "darkgray", (pos[0] * 100, pos[1] * 100, 100, 100), 2)
        for pos in self.world_map]