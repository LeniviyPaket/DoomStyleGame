import pygame as pg
import math
from settings import *


class MiniMap:
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.pos_x = WIDTH - MINIMAP_WIDTH
        self.pos_y = 0
        self.res = MINIMAP_RES
        self.rad = (MINIMAP_WIDTH - 2 * MINIMAP_BORDER) / 2
    
    def draw(self):
        pg.draw.rect(self.game.screen, "black", (self.pos_x, self.pos_y, *self.res))
        pg.draw.rect(self.game.screen, "white", (self.pos_x, self.pos_y, *self.res), MINIMAP_BORDER)
        for x in range(MAP_HEIGHT):
            for y in range(MAP_WIDTH):
                if self.game.map.floor_map[x][y]:
                    pg.draw.rect(self.game.screen, "red" if (x == self.player.floor_x and y == self.player.floor_y) else "white",
                                (self.pos_x + MINIMAP_BORDER + y * MINIMAP_CELL_WIDTH, self.pos_y + MINIMAP_BORDER + x * MINIMAP_CELL_HEIGHT, MINIMAP_CELL_WIDTH, MINIMAP_CELL_HEIGHT), 4)
                                # ((y - self.player.floor_x) % MAP_HEIGHT)
        pg.draw.circle(self.game.screen, "green", (self.pos_x + MINIMAP_WIDTH / 2, self.pos_y + MINIMAP_WIDTH / 2), self.rad, 3)
        pg.draw.line(self.game.screen, "green", (self.pos_x + MINIMAP_WIDTH / 2, self.pos_y + MINIMAP_WIDTH / 2),
                    (self.pos_x + MINIMAP_WIDTH / 2 + self.rad * math.cos(self.player.angle), self.pos_y + MINIMAP_WIDTH / 2 + self.rad * math.sin(self.player.angle)), 3)