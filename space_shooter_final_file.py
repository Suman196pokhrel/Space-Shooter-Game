import pygame
import random
import math
from pygame import mixer

# Bg sound


pygame.init()
clock = pygame.time.Clock()
space_ship_anime_1 = [
    pygame.image.load(r's1.png'), pygame.image.load(r's2.png'), pygame.image.load(r's3.png'),
    pygame.image.load(r's4.png'),
    pygame.image.load(r's5.png'), pygame.image.load(r's6.png'), pygame.image.load(r's7.png'),
    pygame.image.load(r's8.png'),

]

count = 0
mixer.music.load('bg_music.mp3')
mixer.music.play(-1)


class mygame():
    def __init__(self):
        self.height_win = 600
        self.width_win = 500
        self.win = pygame.display.set_mode((self.width_win, self.height_win))
        self.title = pygame.display.set_caption('Self_Taught_test')
        # pygame.display.set_mode(f'{args}')
        self.icon = pygame.image.load('L1.png')
        pygame.display.set_icon(self.icon)
        self.win.fill((33, 32, 65))
        self.player_img = pygame.image.load('s1.png')
        self.playerx = 250
        self.playery = 500
        # self.enemy_img = pygame.image.load('alien.png')
        # self.alienx, self.alieny = random.randint(5, 465), random.randint(5, 325)
        self.player_movement_blocks = 5

        self.bg = pygame.image.load('247.jpg')
        self.bullet_1 = pygame.image.load('final_bull.png')
        self.bulletx, self.bullety = 0, 500
        self.bullet_movement_speed = 20
        self.bullet_state = 'ready'
        self.non_changing_bullet_position_x = 0
        self.non_changing_bullet_position_y = 0
        self.score_value = 0
        # Enemy Lists
        self.enemy_img_list = []
        self.alienx_list = []
        self.alieny_list = []
        self.enemy_movement_speed_list = []
        self.num_of_enemies = 6
        self.alien_img_list = [pygame.image.load(r'alien.png'),
                               pygame.image.load(r'alien1.png'),
                               pygame.image.load(r'alien2.png'),
                               pygame.image.load(r'alien3.png'),
                               pygame.image.load(r'alien4.png'),
                               pygame.image.load(r'alien5.png')
                               ]

        if self.num_of_enemies > len(self.alien_img_list):
            # len11 = len(self.alien_img_list)
            list_loads = True
            while list_loads:
                if self.num_of_enemies > len(self.alien_img_list):
                    self.alien_img_list.append(random.choice(self.alien_img_list))
                else:
                    list_loads = False
        for i in range(self.num_of_enemies):
            self.enemy_img_list.append(self.alien_img_list[i])
            self.alienx_list.append(random.randint(5, 465))
            self.alieny_list.append(random.randint(5, 325))
            self.enemy_movement_speed_list.append(1)

        self.font_for_btn_1 = pygame.font.Font('freesansbold.ttf', 30)
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.over_text_font = pygame.font.Font('freesansbold.ttf', 50)
        self.textX = 5
        self.textY = 20
        self.game_over_text = None
        self.game_statues = 'playing'
        self.btn_width = 150
        self.btn_height = 100

    def player(self):
        self.win.blit(self.player_img, (self.playerx, self.playery))

    def enemy(self):
        for i in range(self.num_of_enemies):
            self.win.blit(self.enemy_img_list[i], (self.alienx_list[i], self.alieny_list[i]))

    def player_actions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.playerx > 5:
            self.playerx -= self.player_movement_blocks
            # self.ship_animation()

        if keys[pygame.K_RIGHT] and self.playerx < 465:
            self.playerx += self.player_movement_blocks
            # self.ship_animation()

        if keys[pygame.K_UP] and self.playery > 5:
            self.playery -= self.player_movement_blocks
            # self.ship_animation()

        if keys[pygame.K_DOWN] and self.playery < 565:
            self.playery += self.player_movement_blocks
            # self.ship_animation()

        if keys[pygame.K_SPACE]:
            if self.bullet_state == 'ready':
                self.ship_animation()
                self.non_changing_bullet_position_x = self.playerx
                self.non_changing_bullet_position_y = self.playery
                bullet = mixer.Sound('gunsound.wav')
                bullet.play()

                self.bullet()

    def enemy_actions(self):
        if self.game_statues != 'over':
            for i in range(self.num_of_enemies):
                if self.alienx_list[i] in range(5, 460):
                    self.alienx_list[i] += self.enemy_movement_speed_list[i]

                elif self.alienx_list[i] >= 460:
                    self.enemy_movement_speed_list[i] = -1
                    self.alieny_list[i] += 15
                    self.alienx_list[i] = 458
                elif self.alienx_list[i] <= 5:
                    self.enemy_movement_speed_list[i] = +1
                    self.alieny_list[i] += 15
                    self.alienx_list[i] = 5

    def bullet(self):

        self.bullet_state = 'fire'
        self.win.blit(self.bullet_1, (self.non_changing_bullet_position_x, self.non_changing_bullet_position_y))

    def bullet_action(self):
        if self.bullet_state == 'fire' and self.non_changing_bullet_position_y > 0:
            self.bullet()
            self.non_changing_bullet_position_y -= self.bullet_movement_speed

        else:
            self.bullety = self.playery
            self.bullet_state = 'ready'

    def collision_detection_bullet_enemies(self):
        if self.game_statues != 'over':
            respawn_list = []
            for i in range(self.num_of_enemies):
                d = math.sqrt((math.pow(self.alienx_list[i] - self.non_changing_bullet_position_x, 2)) + (
                    math.pow(self.alieny_list[i] - self.non_changing_bullet_position_y, 2)))
                if d <= 30:
                    respawn_list.append(i)
                    explosion = mixer.Sound('explosion.wav')
                    explosion.play()
                    # print(respawn_list)
                    self.score_value += 1
                    self.bullety = self.playery
                    self.alienx_list[i] = random.randint(5, 460)
                    self.alieny_list[i] = random.randint(0, 300)

    def score_board(self):
        score = self.font.render(f'Score : {self.score_value}', True, (67, 218, 185))
        self.win.blit(score, (self.textX, self.textY))

    def collision_detection_player_enemies(self):
        for i in range(self.num_of_enemies):
            d = math.sqrt((math.pow(self.alienx_list[i] - self.playerx, 2)) + (
                math.pow(self.alieny_list[i] - self.playery, 2)))

            if d <= 30:
                self.game_statues = 'over'

                # print(respawn_list)
                # self.score_value += 1
                # self.alienx_list[i] = random.randint(5, 460)
                # self.alieny_list[i] = random.randint(0, 300)
                pass

    def game_over(self):
        if self.game_statues == 'over':
            # for i in range(self.num_of_enemies):
            #     self.alienx_list[i]  = 100,100

            self.game_over_text = self.over_text_font.render(f'GAME OVER', True, (67, 218, 185))
            self.win.blit(self.game_over_text, (100, 200))

            self.game_over_text_score = self.over_text_font.render(f'YOUR SCORE :{self.score_value}', True,
                                                                   (67, 218, 185))
            self.win.blit(self.game_over_text_score, (80, 250))

            self.btn = pygame.draw.rect(self.win, (93, 43, 224), (200, 320, self.btn_width, self.btn_height))

            self.btn_text = self.font_for_btn_1.render(f'Try Again', True, (0, 0, 0))
            self.win.blit(self.btn_text, (210, 350))

            if 200 + self.btn_width > pygame.mouse.get_pos()[0] > 200 and 320 + self.btn_height > \
                    pygame.mouse.get_pos()[1] > 320:
                self.btn = pygame.draw.rect(self.win, (133, 112, 194), (200, 320, self.btn_width, self.btn_height))
                self.win.blit(self.btn_text, (210, 350))
                keys = pygame.mouse.get_pressed()
                if keys[0]:
                    self.game_statues = 'playing'
                    for i in range(self.num_of_enemies):
                        self.alienx_list.append(random.randint(5, 465))
                        self.alieny_list.append(random.randint(5, 325))


    def ship_animation(self):
        global count
        if count + 1 >= 32:
            count = 0
        self.win.blit(space_ship_anime_1[count // 4], (self.playerx, self.playery))
        count += 1


# Game Loop
mainwin = mygame()
running = True
while running:

    clock.tick(200)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # print(pygame.event.get())

            running = False
    mainwin.win.fill((33, 32, 65))
    mainwin.win.blit(mainwin.bg, (0, 0))
    mainwin.player()
    mainwin.player_actions()

    mainwin.bullet_action()

    mainwin.enemy()
    mainwin.enemy_actions()

    mainwin.collision_detection_bullet_enemies()
    mainwin.score_board()
    mainwin.collision_detection_player_enemies()
    mainwin.ship_animation()
    mainwin.game_over()


    pygame.display.update()
