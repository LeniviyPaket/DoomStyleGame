from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.floor_y, self.floor_x = PLAYER_POS_FLOOR
        self.angle = PLAYER_ANGLE
    
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
        
        self.check_wall_collision(dx, dy) #check collisions with walls & move if none

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau
    
    def check_walls(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        self.move_to_neighbor_room(int(self.x + dx), int(self.y + dy))
        if self.check_walls(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_walls(int(self.x), int(self.y + dy)):
            self.y += dy
    #toadd: hitbox for room traversion (add 'd' in map layout for door)

    def move_to_neighbor_room(self, x, y):
        if self.game.map.mini_map[y][x] == 'd':
            print('I tried', x, y, self.floor_x, self.floor_y)
            if y == 0:
                if self.game.map.floor_map[(self.floor_x - 1) % MAP_HEIGHT][self.floor_y]:
                    self.floor_x = (self.floor_x - 1) % MAP_HEIGHT
                    self.y = 7.8
            if y == 8:
                if self.game.map.floor_map[(self.floor_x + 1) % MAP_HEIGHT][self.floor_y]:
                    self.floor_x = (self.floor_x + 1) % MAP_HEIGHT
                    self.y = 1.2
            if x == 0:
                if self.game.map.floor_map[self.floor_x][(self.floor_y - 1) % MAP_WIDTH]:
                    self.floor_y = (self.floor_y - 1) % MAP_WIDTH
                    self.x = 14.8
            if x == 15:
                if self.game.map.floor_map[self.floor_x][(self.floor_y + 1) % MAP_WIDTH]:
                    self.floor_y = (self.floor_y + 1) % MAP_WIDTH
                    self.x = 1.2
            self.game.map.load_new_room()

    def draw(self):
        # pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #             (self.x * 100 + WIDTH * math.cos(self.angle),
        #             self.y * 100 + HEIGHT * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()
    
    def pos(self):
        return self.x, self.y
    
    def map_pos(self):
        return int(self.x), int(self.y)
    