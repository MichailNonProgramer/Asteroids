import math
import pygame

class Bullet:
    def __init__(self, x, y, direction, bullet_speed, color, gameDisplay, display_width, display_height):
        self.x = x
        self.y = y
        self.dir = direction
        self.life = 30
        self.color = color
        self.bullet_speed = bullet_speed
        self.gameDisplay = gameDisplay
        self.display_width = display_width
        self.display_height = display_height

    def update_bullet(self):
        # Moving
        self.x += self.bullet_speed * math.cos(self.dir * math.pi / 180)
        self.y += self.bullet_speed * math.sin(self.dir * math.pi / 180)

        # Drawing
        pygame.draw.circle(self.gameDisplay, self.color, (int(self.x), int(self.y)), 2)

        # Wrapping
        if self.x > self.display_width:
            self.x = 0
        elif self.x < 0:
            self.x = self.display_width
        elif self.y > self.display_height:
            self.y = 0
        elif self.y < 0:
            self.y = self.display_height
        self.life -= 1