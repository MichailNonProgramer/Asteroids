import math
from random import random

import pygame


class BlackHolle:
    def __init__(self, x, y, display_width, display_height, gameDisplay, color):
        self.x = x
        self.y = y
        self.display_width = display_width
        self.display_height = display_height
        self.gameDisplay = gameDisplay
        self.color = color
        self.size = 50
        self.size_gravity_field = 150
        self.rotate = 3
        self.shift = 0.85
        self.angle_one_sector = 45
        self.angle_two_sector = 135
        self.angle_thre_sector = 225
        self.angle_four_sector = 315

    def update(self):
        # Draw
        pygame.draw.circle(self.gameDisplay, self.color, (int(self.x), int(self.y)), int(self.size/2), 1)

    def pull_object(self, object_x, object_y, object_dir):
        x = self.x - object_x
        y = self.y - object_y
        radius = math.sqrt(x *x + y * y)
        if (radius < self.size_gravity_field):
            if (x >= 0 and y >= 0):
                if object_dir >= 45 and object_dir < 225:
                    object_dir -= self.rotate
                else:
                    object_dir += self.rotate
                object_x += self.shift
                object_y += self.shift
            if (x >= 0 and y < 0):
                if object_dir >= 135 and object_dir < 315:
                    object_dir += self.rotate
                else:
                    object_dir -= self.rotate
                object_x += self.shift
                object_y -= self.shift
            if (x < 0 and y >= 0):
                if object_dir >= 45 and object_dir < 225:
                    object_dir += self.rotate
                else:
                    object_dir -= self.rotate
                object_x -= self.shift
                object_y += self.shift
            if (x < 0 and y < 0):
                if object_dir >= 135 and object_dir < 315:
                    object_dir += self.rotate
                else:
                    object_dir -= self.rotate
                object_x -= self.shift
                object_y -= self.shift
        return object_dir, object_x, object_y