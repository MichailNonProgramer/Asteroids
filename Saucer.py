import math
import pygame
import random
import Bullet

pygame.init()
snd_saucerB = pygame.mixer.Sound("Sounds/saucerBig.wav")
snd_saucerS = pygame.mixer.Sound("Sounds/saucerSmall.wav")

class Saucer:
    def __init__(self, saucer_speed, display_height, display_width, gameDisplay, color, bullet_speed, player):
        self.x = 0
        self.y = 0
        self.state = "Dead"
        self.type = "Large"
        self.dirchoice = ()
        self.bullets = []
        self.cd = 0
        self.bdir = 0
        self.soundDelay = 0
        self.color = color
        self.saucer_speed = saucer_speed
        self.display_height = display_height
        self.display_width = display_width
        self.gameDisplay = gameDisplay
        self.bullet_speed = bullet_speed
        self.player = player

    def update_saucer(self):
        self.x += self.saucer_speed * math.cos(self.dir * math.pi / 180)
        self.y += self.saucer_speed * math.sin(self.dir * math.pi / 180)
        if random.randrange(0, 100) == 1:
            self.dir = random.choice(self.dirchoice)

        if self.y < 0:
            self.y = self.display_height
        elif self.y > self.display_height:
            self.y = 0
        if self.x < 0 or self.x > self.display_width:
            self.state = "Dead"

        if self.type == "Large":
            self.bdir = random.randint(0, 360)
        if self.cd == 0 and not self.player.invulnerability:
            self.bullets.append(Bullet.Bullet(self.x, self.y, self.bdir,self.bullet_speed, self.color,self.gameDisplay,
                                              self.display_width, self.display_height))
            self.cd = 30
        else:
            self.cd -= 1

        # Play SFX
        if self.type == "Large":
            pygame.mixer.Sound.play(snd_saucerB)
        else:
            pygame.mixer.Sound.play(snd_saucerS)

    def create_saucer(self):
        self.state = "Alive"

        # Set random position
        self.x = random.choice((0, self.display_width))
        self.y = random.randint(0, self.display_height)

        # Set random type
        if random.randint(0, 1) == 0:
            self.type = "Large"
            self.size = 20
        else:
            self.type = "Small"
            self.size = 10

        # Create random direction
        if self.x == 0:
            self.dir = 0
            self.dirchoice = (0, 45, -45)
        else:
            self.dir = 180
            self.dirchoice = (180, 135, -135)

        # Reset bullet cooldown
        self.cd = 0

    def draw_saucer(self):
        # Draw saucer
        pygame.draw.polygon(self.gameDisplay, self.color,
                            ((self.x + self.size, self.y),
                             (self.x + self.size / 2, self.y + self.size / 3),
                             (self.x - self.size / 2, self.y + self.size / 3),
                             (self.x - self.size, self.y),
                             (self.x - self.size / 2, self.y - self.size / 3),
                             (self.x + self.size / 2, self.y - self.size / 3)), 1)
        pygame.draw.line(self.gameDisplay, self.color,
                         (self.x - self.size, self.y),
                         (self.x + self.size, self.y))
        pygame.draw.polygon(self.gameDisplay, self.color,
                            ((self.x - self.size / 2, self.y - self.size / 3),
                             (self.x - self.size / 3, self.y - 2 * self.size / 3),
                             (self.x + self.size / 3, self.y - 2 * self.size / 3),
                             (self.x + self.size / 2, self.y - self.size / 3)), 1)