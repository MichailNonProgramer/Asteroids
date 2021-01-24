import pygame
import random
import math
import Player
import Saucer
import Bullet
import Asteroid
import InputBox
import BlackHolle
from operator import itemgetter

class Game:
    pygame.display.set_caption("Asteroids")

    def __init__(self):
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.blue = (0,0,255)

        self.display_width = 800
        self.display_height = 600

        self.player_size = 10
        self.fd_fric = 0.5
        self.bd_fric = 0.1
        self.player_max_speed = 20
        self.player_max_rtspd = 10
        self.bullet_speed = 15
        self.saucer_speed = 5
        self.small_saucer_accuracy = 10
        self.lvl = 0
        self.lvl_counter = 20
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        self.timer = pygame.time.Clock()
        self.snd_fire = pygame.mixer.Sound("Sounds/fire.wav")
        self.snd_bangL = pygame.mixer.Sound("Sounds/bangLarge.wav")
        self.snd_bangM = pygame.mixer.Sound("Sounds/bangMedium.wav")
        self.snd_bangS = pygame.mixer.Sound("Sounds/bangSmall.wav")
        self.snd_extra = pygame.mixer.Sound("Sounds/extra.wav")
        self.snd_super_fire = pygame.mixer.Sound("Sounds/superFire.wav")
        self.snd_rip = pygame.mixer.Sound("Sounds/rip.wav")
        self.snd_write_record = pygame.mixer.Sound("Sounds/menu.wav")

    def add_shoot(self, bullets, player, angle):
        bullets.append(
                    Bullet.Bullet(player.x, player.y, player.dir + angle, self.bullet_speed, self.white, self.gameDisplay,
                                    self.display_width, self.display_height))
        return bullets


    def game_loop(self, startingState):
        # Init variables
        gameState = startingState
        player_state = "Alive"
        player_blink = 0
        player_pieces = []
        player_dying_delay = 0
        player_invi_dur = 0
        hyperspace = 0
        next_level_delay = 0
        bullet_capacity = 8
        bullets = []
        asteroids = []
        stage = 3
        score = 0
        live = 2
        one_up_multiplier = 1
        intensity = 0
        counter_records = 1
        text_input = InputBox.TextInput()
        player = Player.Player(self.display_width / 2, self.display_height / 2, self.display_width, self.display_height,
                               self.gameDisplay,
                               self.white)
        saucer = Saucer.Saucer(self.saucer_speed, self.display_height, self.display_width, self.gameDisplay, self.white,
                               self.bullet_speed, player)
        black_holle = BlackHolle.BlackHolle(500, 200, self.display_width, self.display_height, self.gameDisplay, self.white)

        # Main loop
        while gameState != "Exit":
            # Game menu
            while gameState == "Menu":
                self.gameDisplay.fill(self.black)
                self.draw_text("ASTEROIDS", self.white, self.display_width / 2, self.display_height / 2, 100)
                self.draw_text("Press any key to START", self.white, self.display_width / 2,
                               self.display_height / 2 + 100, 50)
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        gameState = "Exit"
                    if event.type == pygame.KEYDOWN:
                        gameState = "Playing"
                pygame.display.update()
                self.timer.tick(5)

            while gameState == "Input record":
                self.gameDisplay.fill(self.black)
                self.draw_text("Input your name and press SPACE to continue",
                               self.white, self.display_width / 2, self.display_height / 2, 20)
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        gameState = "Exit"
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            player.name = text_input.get_text()
                            self.save_record(player.name, score)
                            gameState = "Read records"
                text_input.update(events)
                self.gameDisplay.blit(text_input.get_surface(), (self.display_width / 2, self.display_height / 2 + 100))
                pygame.display.update()
                self.timer.tick(5)

            while gameState == "Read records":
                self.gameDisplay.fill(self.black)
                self.draw_text("Records",
                               self.white, self.display_width / 2, 20, 35)
                rec = self.read_records()
                for i in rec:
                    if counter_records == 11:
                        break
                    self.draw_text(str(counter_records) + " " + i[0] + " " + str(i[1]),
                                    self.white, self.display_width / 2, counter_records * 50, 23)
                    counter_records += 1
                self.draw_text("Press anu key to continue",
                               self.white, self.display_width / 2, self.display_height - 50, 35)
                counter_records = 1
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        gameState = "Exit"
                    if event.type == pygame.KEYDOWN:
                        gameState = "Game Over"
                pygame.display.update()
                self.timer.tick(5)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    gameState = "Exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player.thrust = True
                    if event.key == pygame.K_LEFT:
                        player.rtspd = -self.player_max_rtspd
                    if event.key == pygame.K_RIGHT:
                        player.rtspd = self.player_max_rtspd
                        #shoot
                    if event.key == pygame.K_SPACE and player_dying_delay == 0 and len(bullets) < bullet_capacity:
                        bullets = self.add_shoot(bullets,player,0)
                        if player.super_shot:
                            bullets = self.add_shoot(bullets,player, 90)
                            bullets = self.add_shoot(bullets, player, -90)
                            bullets = self.add_shoot(bullets, player, 180)
                            player.super_shot = False
                            pygame.mixer.Sound.play(self.snd_super_fire)
                        else:
                            pygame.mixer.Sound.play(self.snd_fire)
                    if gameState == "Game Over":
                        if event.key == pygame.K_r:
                            gameState = "Exit"
                            self.game_loop("Playing")
                    if event.key == pygame.K_LSHIFT:
                        hyperspace = 30
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player.thrust = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.rtspd = 0

            player.update_player()
            player.dir, player.x, player.y = black_holle.pull_object(player.x, player.y, player.dir)

            if player_invi_dur != 0:
                player_invi_dur -= 1
            elif hyperspace == 0:
                player_state = "Alive"
            self.gameDisplay.fill(self.black)

            if hyperspace != 0:
                player_state = "Died"
                hyperspace -= 1
                if hyperspace == 1:
                    player.x = random.randrange(0, self.display_width)
                    player.y = random.randrange(0, self.display_height)

            for a in asteroids:
                a.update_asteroid()
                a.dir, a.x, a.y = black_holle.pull_object(a.x, a.y, a.dir)
                if player_state != "Died":
                    if self.colliding(player.x, player.y, a.x, a.y, a.size):
                        player_state = "Died"
                        player_dying_delay = 30
                        player_invi_dur = 120
                        player.kill_player()
                        if live != 0:
                            live -= 1
                            pygame.mixer.Sound.play(self.snd_rip)
                        else:
                            self.lvl = 0
                            gameState = "Input record"
                            pygame.mixer.Sound.play(self.snd_write_record)
                        if a.t == "Large":
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Normal", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Normal", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            score += 20
                            player.score_add(20)
                            pygame.mixer.Sound.play(self.snd_bangL)
                        elif a.t == "Normal":
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Small", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Small", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            score += 50
                            player.score_add(50)
                            pygame.mixer.Sound.play(self.snd_bangM)
                        else:
                            score += 100
                            player.score_add(100)
                            pygame.mixer.Sound.play(self.snd_bangS)
                        asteroids.remove(a)

            for f in player_pieces:
                f.update_dead_player()
                if f.x > self.display_width or f.x < 0 or f.y > self.display_height or f.y < 0:
                    player_pieces.remove(f)

            # Check for end of stage
            if len(asteroids) == 0 and saucer.state == "Dead":
                if next_level_delay < 30:
                    next_level_delay += 1
                else:
                    self.lvl += 1
                    stage += 1
                    intensity = 0
                    for i in range(stage):
                        xTo = self.display_width / 2
                        yTo = self.display_height / 2
                        while xTo - self.display_width / 2 < self.display_width / 4 and yTo - self.display_height / 2 < self.display_height / 4:
                            xTo = random.randrange(0, self.display_width)
                            yTo = random.randrange(0, self.display_height)
                        asteroids.append(
                            Asteroid.Asteroid(xTo, yTo, "Large", self.display_width, self.display_height, self.gameDisplay, self.white))
                    next_level_delay = 0
            if intensity < stage * 450:
                intensity += 1

            if saucer.state == "Dead":
                if random.randint(0, 6000) <= (intensity * 2) / (stage * 9) and next_level_delay == 0:
                    saucer.create_saucer()
                    if score >= 4000:
                        saucer.type = "Small"
            else:
                acc = self.small_saucer_accuracy * 4 / stage
                saucer.bdir = math.degrees(math.atan2(-saucer.y + player.y, -saucer.x + player.x) + math.radians(
                    random.uniform(acc, -acc)))

                saucer.update_saucer()
                saucer.draw_saucer()
                saucer.dir, saucer.x, saucer.y = black_holle.pull_object(saucer.x, saucer.y, saucer.dir)

                # Check for collision w/ asteroid
                for a in asteroids:
                    a.dir, a.x, a.y = black_holle.pull_object(a.x, a.y, a.dir)
                    if self.colliding(saucer.x, saucer.y, a.x, a.y, a.size + saucer.size):
                        saucer.state = "Dead"
                        if a.t == "Large":
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Normal", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Normal", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            pygame.mixer.Sound.play(self.snd_bangL)
                        elif a.t == "Normal":
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Small", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Small", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            pygame.mixer.Sound.play(self.snd_bangM)
                        else:
                            pygame.mixer.Sound.play(self.snd_bangS)
                        asteroids.remove(a)

                # Check for collision w/ bullet
                for b in bullets:
                    if self.colliding(b.x, b.y, saucer.x, saucer.y, saucer.size):
                        if saucer.type == "Large":
                            score += 200
                            player.score_add(200)
                        else:
                            score += 1000
                            player.score_add(1000)
                        saucer.state = "Dead"
                        pygame.mixer.Sound.play(self.snd_bangL)
                        bullets.remove(b)


                # Check collision w/ player
                if self.colliding(saucer.x, saucer.y, player.x, player.y, saucer.size):
                    if player_state != "Died":
                        if player.shield:
                            player.shield = False
                        else:
                            player_state = "Died"
                            player_dying_delay = 30
                            player_invi_dur = 120
                            player.kill_player()
                            if live != 0:
                                live -= 1
                                pygame.mixer.Sound.play(self.snd_rip)
                            else:
                                self.lvl = 0
                                gameState = "Input record"
                                pygame.mixer.Sound.play(self.snd_write_record)
                            pygame.mixer.Sound.play(self.snd_bangL)
                for b in saucer.bullets:
                    b.update_bullet()
                    b.dir, b.x, b.y = black_holle.pull_object(b.x, b.y, b.dir)

                    # Check for collision w/ asteroids
                    for a in asteroids:
                        if self.colliding(b.x, b.y, a.x, a.y, a.size):
                            # Split asteroid
                            if a.t == "Large":
                                asteroids.append(
                                    Asteroid.Asteroid(a.x, a.y, "Normal", self.display_width, self.display_height,
                                                      self.gameDisplay, self.white))
                                asteroids.append(
                                    Asteroid.Asteroid(a.x, a.y, "Normal", self.display_width, self.display_height,
                                                      self.gameDisplay, self.white))
                                pygame.mixer.Sound.play(self.snd_bangL)
                            elif a.t == "Normal":
                                asteroids.append(
                                    Asteroid.Asteroid(a.x, a.y, "Small", self.display_width, self.display_height,
                                                      self.gameDisplay, self.white))
                                asteroids.append(
                                    Asteroid.Asteroid(a.x, a.y, "Small", self.display_width, self.display_height,
                                                      self.gameDisplay, self.white))
                                pygame.mixer.Sound.play(self.snd_bangL)
                            else:
                                pygame.mixer.Sound.play(self.snd_bangL)
                            asteroids.remove(a)
                            saucer.bullets.remove(b)

                            break

                    # Check for collision w/ player
                    if self.colliding(player.x, player.y, b.x, b.y, 5):
                        if player_state != "Died":
                            if player.shield:
                                player.shield = False
                            else:
                                player_state = "Died"
                                player_dying_delay = 30
                                player_invi_dur = 120
                                player.kill_player()

                                if live != 0:
                                    live -= 1
                                    pygame.mixer.Sound.play(self.snd_rip)
                                else:
                                    gameState = "Input record"
                                    pygame.mixer.Sound.play(self.snd_write_record)
                                pygame.mixer.Sound.play(self.snd_bangL)

                            # Remove bullet
                            saucer.bullets.remove(b)

                    if b.life <= 0:
                        try:
                            saucer.bullets.remove(b)
                        except ValueError:
                            continue

            # Bullets
            for b in bullets:
                # Update bullets
                b.update_bullet()
                b.dir, b.x, b.y = black_holle.pull_object(b.x, b.y, b.dir)
                # Check for bullets collide w/ asteroid
                for a in asteroids:
                    if b.x > a.x - a.size and b.x < a.x + a.size and b.y > a.y - a.size and b.y < a.y + a.size:
                        # Split asteroid
                        if a.t == "Large":
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Normal", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Normal", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            score += 20
                            player.score_add(20)
                            pygame.mixer.Sound.play(self.snd_bangL)
                        elif a.t == "Normal":
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Small", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            asteroids.append(
                                Asteroid.Asteroid(a.x, a.y, "Small", self.display_width, self.display_height, self.gameDisplay,
                                                  self.white))
                            score += 50
                            player.score_add(50)
                            pygame.mixer.Sound.play(self.snd_bangM)
                        else:
                            score += 100
                            player.score_add(100)
                            pygame.mixer.Sound.play(self.snd_bangS)
                        asteroids.remove(a)
                        bullets.remove(b)

                        break
                if b.life <= 0:
                    try:
                        bullets.remove(b)
                    except ValueError:
                        continue
            for b in bullets:
                if self.colliding(b.x, b.y, black_holle.x, black_holle.y, black_holle.size/2):
                    bullets.remove(b)

            for b in asteroids:
                if self.colliding(b.x, b.y, black_holle.x, black_holle.y, black_holle.size/2):
                    asteroids.remove(b)

            if self.colliding(saucer.x, saucer.y, black_holle.x, black_holle.y, black_holle.size/2):
                saucer.state = "Dead"

            if self.colliding(player.x, player.y, black_holle.x, black_holle.y, black_holle.size/2):
                player_state = "Died"
                player_dying_delay = 30
                player_invi_dur = 120
                player.kill_player()
                if live != 0:
                    live -= 1
                    pygame.mixer.Sound.play(self.snd_rip)
                else:
                    self.lvl = 0
                    gameState = "Input record"
                    pygame.mixer.Sound.play(self.snd_write_record)

            if score > one_up_multiplier * 10000:
                one_up_multiplier += 1
                if live <= 5:
                 live += 1
            # Draw player
            if gameState != "Game Over":
                if player_state == "Died":
                    if hyperspace == 0:
                        if player_dying_delay == 0:
                            if player_blink < 5:
                                if player_blink == 0:
                                    player_blink = 10
                                else:
                                    player.draw_player()
                            player_blink -= 1
                        else:
                            player_dying_delay -= 1
                else:
                    player.draw_player()
            else:
                self.draw_text("Game Over", self.white, self.display_width / 2, self.display_height / 2, 100)
                self.draw_text("Press \"R\" to restart!", self.white, self.display_width / 2, self.display_height / 2 + 100, 50)
                live = -1

            self.draw_text(str(score), self.white, 60, 20, 40, False)
            self.draw_text(str("Level " + str(self.lvl)), self.white, self.display_width - 140, 20, 40, False)
            self.draw_text(str(player.super_shot_counter), self.red, self.display_width - 50, self.display_height / 2 - 50, 20, False)
            self.draw_text(str(player.shield_counter), self.blue, self.display_width - 50, self.display_height / 2, 20, False)
            self.draw_text(str(player.invulnerability_counter), self.white, self.display_width - 50, self.display_height / 2 + 50, 20, False)
            self.draw_text(str(player.invulnerability_count), self.white, self.display_width - 50,
                           self.display_height / 2 + 65, 10, False)

            for l in range(live + 1):
                Player.Player(75 + l * 25, 75, self.display_width, self.display_height, self.gameDisplay, self.white).draw_player()

            if player.invulnerability_count != 0:
                player.invulnerability_count -= 1
            else:
                player.invulnerability = False
            black_holle.update()

            pygame.display.update()
            self.timer.tick(30)

    def draw_text(self, msg, color, x, y, s, center=True):
        screen_text = pygame.font.SysFont("Calibri", s).render(msg, True, color)
        if center:
            rect = screen_text.get_rect()
            rect.center = (x, y)
        else:
            rect = (x, y)
        self.gameDisplay.blit(screen_text, rect)

    # Create funtion to chek for collision
    def colliding(self, x, y, xTo, yTo, size):
        if x > xTo - size and x < xTo + size and y > yTo - size and y < yTo + size:
            return True
        return False

    def save_record(self, name, score):
        with open("records.txt", "a") as file:
            file.write(name + "///" + str(score) + " " + "\n")

    def read_records(self):
        records = list()
        with open("records.txt", "r") as f:
             for line in f.readlines():
                 records.append((line.rstrip().split('///')[0],int(line.rstrip().split('///')[1])))
        res = sorted(records, key=itemgetter(1), reverse=True)
        return res