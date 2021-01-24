import math
import pygame


class Player:
    def __init__(self, x, y, display_width,
                 display_height, gameDisplay, color):
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.dir = -90
        self.rtspd = 0
        self.thrust = False
        self.fd_fric = 0.5
        self.bd_fric = 0.1
        self.player_max_speed = 20
        self.player_size = 10
        self.shield = False
        self.super_shot = False
        self.invulnerability = False
        self.shield_counter = 0
        self.super_shot_counter = 0
        self.invulnerability_counter = 0
        self.invulnerability_count = 0
        self.display_width = display_width
        self.display_height = display_height
        self.gameDisplay = gameDisplay
        self.color = color
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        self.name = ""

    def update_player(self):
        speed = math.sqrt(self.hspeed**2 + self.vspeed**2)
        if self.thrust:
            if speed + self.fd_fric < self.player_max_speed:
                self.hspeed += self.fd_fric \
                               * math.cos(self.dir * math.pi / 180)
                self.vspeed += self.fd_fric \
                               * math.sin(self.dir * math.pi / 180)
            else:
                self.hspeed = self.player_max_speed \
                              * math.cos(self.dir * math.pi / 180)
                self.vspeed = self.player_max_speed \
                              * math.sin(self.dir * math.pi / 180)
        else:
            if speed - self.bd_fric > 0:
                change_in_hspeed = (self.bd_fric
                                    * math.cos(self.vspeed / self.hspeed))
                change_in_vspeed = (self.bd_fric
                                    * math.sin(self.vspeed / self.hspeed))
                if self.hspeed != 0:
                    if change_in_hspeed / abs(change_in_hspeed) == self.hspeed / abs(self.hspeed):
                        self.hspeed -= change_in_hspeed
                    else:
                        self.hspeed += change_in_hspeed
                if self.vspeed != 0:
                    if change_in_vspeed / abs(change_in_vspeed) == self.vspeed / abs(self.vspeed):
                        self.vspeed -= change_in_vspeed
                    else:
                        self.vspeed += change_in_vspeed
            else:
                self.hspeed = 0
                self.vspeed = 0
        self.x += self.hspeed
        self.y += self.vspeed

        if self.x > self.display_width:
            self.x = 0
        elif self.x < 0:
            self.x = self.display_width
        elif self.y > self.display_height:
            self.y = 0
        elif self.y < 0:
            self.y = self.display_height
        self.dir += self.rtspd

    def set_x(self):
        return self.x

    def set_y(self):
        return self.y

    def draw_player(self):
        a = math.radians(self.dir)
        x = self.x
        y = self.y
        s = self.player_size
        t = self.thrust
        if self.super_shot:
            self.color = self.red
        else:
            self.color = self.white
        # Draw player
        pygame.draw.line(self.gameDisplay, self.color,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) + a),
                          y - (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) + a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(self.gameDisplay, self.color,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) - a),
                          y + (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) - a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(self.gameDisplay, self.color,
                         (x - (s * math.sqrt(2) / 2) * math.cos(a + math.pi / 4),
                          y - (s * math.sqrt(2) / 2) * math.sin(a + math.pi / 4)),
                         (x - (s * math.sqrt(2) / 2) * math.cos(-a + math.pi / 4),
                          y + (s * math.sqrt(2) / 2) * math.sin(-a + math.pi / 4)))
        if self.shield:
            pygame.draw.line(self.gameDisplay, self.blue,
                             (x - 1.5*(s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) + a),
                              y - 1.5*(s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) + a)),
                             (x + 1.5* s * math.cos(a), y + s * math.sin(a)))

            pygame.draw.line(self.gameDisplay, self.blue,
                             (x - 1.5*(s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) - a),
                              y + 1.5*(s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) - a)),
                             (x + 1.5*s * math.cos(a), y + s * math.sin(a)))

            pygame.draw.line(self.gameDisplay, self.blue,
                             (x - 1.5*(s * math.sqrt(2) / 2) * math.cos(a + math.pi / 4),
                              y - 1.5*(s * math.sqrt(2) / 2) * math.sin(a + math.pi / 4)),
                             (x - 1.5*(s * math.sqrt(2) / 2) * math.cos(-a + math.pi / 4),
                              y + 1.5*(s * math.sqrt(2) / 2) * math.sin(-a + math.pi / 4)))

        if self.invulnerability:
            pygame.draw.circle(self.gameDisplay, self.white, (int(x) , int(y)), 15, 1)

        if t:
            pygame.draw.line(self.gameDisplay, self.color,
                             (x - s * math.cos(a),
                              y - s * math.sin(a)),
                             (x - (s * math.sqrt(5) / 4) * math.cos(a + math.pi / 6),
                              y - (s * math.sqrt(5) / 4) * math.sin(a + math.pi / 6)))
            pygame.draw.line(self.gameDisplay, self.color,
                             (x - s * math.cos(-a),
                              y + s * math.sin(-a)),
                             (x - (s * math.sqrt(5) / 4) * math.cos(-a + math.pi / 6),
                              y + (s * math.sqrt(5) / 4) * math.sin(-a + math.pi / 6)))

    def kill_player(self):
        self.x = self.display_width / 2
        self.y = self.display_height / 2
        self.thrust = False
        self.dir = -90
        self.hspeed = 0
        self.vspeed = 0
        self.bonus_off()

    def bonus_activated(self):
        if self.shield_counter >= 500:
            self.shield = True
            self.shield_counter = 0
        if self.super_shot_counter >= 1000:
            self.super_shot = True
            self.super_shot_counter = 0
        if self.invulnerability_counter >= 2000:
            self.invulnerability = True
            self.invulnerability_count = 300
            self.invulnerability_counter = 0

    def bonus_off(self):
        self.shield = False
        self.super_shot = False
        self.invulnerability = False

    def score_add(self, count):
        if not self.shield:
            self.shield_counter += count
        if not self.super_shot:
            self.super_shot_counter += count
        if not self.invulnerability:
            self.invulnerability_counter += count
        self.bonus_activated()


