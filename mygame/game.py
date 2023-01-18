import random
import pygame
import os

# Главный экран
pygame.init()
win_height = 400
win_width = 800
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('defender')
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

hero = pygame.image.load(os.path.join('stand.png'))
hero = pygame.transform.scale(hero, (100, 200))
first_bg = pygame.image.load(os.path.join('first_bg.jpg'))
first_bg = pygame.transform.scale(first_bg, (win_width, win_height))

run2 = True
while run2:
    # выход из игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run2 = False
    k_key = pygame.key.get_pressed()
    win.blit(first_bg, (0, 0))

    font = pygame.font.Font('freesansbold.ttf', 20)
    t1 = font.render('Добро пожаловать в игру defender', True, white)
    t2 = font.render('На вас, солдат, возложена большая ответственность,', True, white)
    t3 = font.render('а именно, защита башни от чудовищ.', True, white)
    t4 = font.render('Удачи вам в бою', True, white)
    t5 = font.render('Нажмите пробел чтобы начать', True, white)

    win.blit(t1, (0, 0))
    win.blit(t2, (0, 30))
    win.blit(t3, (0, 60))
    win.blit(t4, (0, 90))
    win.blit(t5, (200, 300))
    win.blit(hero, (600, 130))
    pygame.display.update()
    if k_key[pygame.K_SPACE]:
        pygame.init()
        win_height = 400
        win_width = 800
        win = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption('defender')

        # спрайты
        left = [pygame.image.load(os.path.join("L_1.png")),
                pygame.image.load(os.path.join("L_2.png")),
                pygame.image.load(os.path.join("L_3.png")),
                pygame.image.load(os.path.join("L_4.png")),
                pygame.image.load(os.path.join("L_5.png")),
                pygame.image.load(os.path.join("L_6.png")),
                pygame.image.load(os.path.join("L_7.png")),
                pygame.image.load(os.path.join("L_8.png")),
                pygame.image.load(os.path.join("L_9.png"))
                ]
        right = [pygame.image.load(os.path.join("r_1.png")),
                 pygame.image.load(os.path.join("r_2.png")),
                 pygame.image.load(os.path.join("r_3.png")),
                 pygame.image.load(os.path.join("r_4.png")),
                 pygame.image.load(os.path.join("r_5.png")),
                 pygame.image.load(os.path.join("r_6.png")),
                 pygame.image.load(os.path.join("r_7.png")),
                 pygame.image.load(os.path.join("r_8.png")),
                 pygame.image.load(os.path.join("r_9.png"))
                 ]
        enemy_left = [pygame.image.load(os.path.join('enemy_left_1.png')),
                      pygame.image.load(os.path.join('enemy_left_2.png')),
                      pygame.image.load(os.path.join('enemy_left_3.png')),
                      pygame.image.load(os.path.join('enemy_left_4.png')),
                      pygame.image.load(os.path.join('enemy_left_5.png')),
                      pygame.image.load(os.path.join('enemy_left_6.png')),
                      pygame.image.load(os.path.join('enemy_left_7.png')),
                      pygame.image.load(os.path.join('enemy_left_8.png')),
                      pygame.image.load(os.path.join('enemy_left_9.png')),
                      pygame.image.load(os.path.join('enemy_left_10.png')),
                      pygame.image.load(os.path.join('enemy_left_11.png'))
                      ]
        enemy_right = [pygame.image.load(os.path.join('enemy_right_1.png')),
                       pygame.image.load(os.path.join('enemy_right_2.png')),
                       pygame.image.load(os.path.join('enemy_right_3.png')),
                       pygame.image.load(os.path.join('enemy_right_4.png')),
                       pygame.image.load(os.path.join('enemy_right_5.png')),
                       pygame.image.load(os.path.join('enemy_right_6.png')),
                       pygame.image.load(os.path.join('enemy_right_7.png')),
                       pygame.image.load(os.path.join('enemy_right_8.png')),
                       pygame.image.load(os.path.join('enemy_right_9.png')),
                       pygame.image.load(os.path.join('enemy_right_10.png')),
                       pygame.image.load(os.path.join('enemy_right_11.png'))
                       ]
        bg = pygame.image.load('screen.png')
        background = pygame.transform.scale(bg, (win_width, win_height))
        bullet_img = pygame.image.load(os.path.join('ball.png'))
        bullet_img = pygame.transform.scale(bullet_img, (20, 20))
        tower = pygame.image.load(os.path.join('tower.png'))
        tower = pygame.transform.scale(tower, (110, 200))
        boost_img = pygame.image.load(os.path.join('boost.png'))
        boost_img = pygame.transform.scale(boost_img, (20, 20))
        pygame.mixer.music.load('bg_music.mp3')
        pygame.mixer.music.play(-1)
        shoot_sound = pygame.mixer.Sound('shootinng.mp3')

        green = (0, 255, 0)
        black = (0, 0, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)


        class Hero:
            def __init__(self, x, y):
                # ходьба
                self.x = x
                self.y = y
                self.velx = 10
                self.vely = 10
                self.face_right = True
                self.face_left = False
                self.stepIndex = 0

                self.jump = False
                self.bullets = []
                self.cool_down_count = 0
                self.hitbox = (self.x, self.y, 20, 64)
                self.health = 30
                self.lives = 2
                self.alive = True
                self.remove_boost = False
                self.damage = 6.5

            def move_hero(self, key):
                # движение
                if key[pygame.K_RIGHT] and self.x <= win_width - 62:
                    self.x += self.velx
                    self.face_right = True
                    self.face_left = False
                elif key[pygame.K_LEFT] and self.x >= 0:
                    self.x -= self.velx
                    self.face_right = False
                    self.face_left = True
                else:
                    self.stepIndex = 0

            def draw(self, win):
                self.hitbox = (self.x + 30, self.y, 10, 60)
                pygame.draw.rect(win, red, (self.x, self.y - 10, 30, 10))
                if self.health >= 0:
                    pygame.draw.rect(win, green, (self.x, self.y - 10, self.health, 10))
                if self.stepIndex >= 9:
                    self.stepIndex = 0
                if self.face_left:
                    win.blit(left[self.stepIndex], (self.x, self.y))
                    self.stepIndex += 1
                if self.face_right:
                    win.blit(right[self.stepIndex], (self.x, self.y))
                    self.stepIndex += 1

            def jump_motion(self, key):
                # прыжок
                if key[pygame.K_SPACE] and self.jump is False:
                    self.jump = True
                if self.jump:
                    self.y -= self.vely*3.5
                    self.vely -= 2
                if self.vely < -10:
                    self.jump = False
                    self.vely = 10

            def direction(self):
                if self.face_right:
                    return 1
                if self.face_left:
                    return -1

            def cooldown(self):
                if self.cool_down_count >= 20:
                    self.cool_down_count = 0
                elif self.cool_down_count > 0:
                    self.cool_down_count += 1.7

            def shoot(self):
                self.cooldown()
                self.hit()
                if key[pygame.K_f] and self.cool_down_count == 0:
                    shoot_sound.play()
                    bullet = Bullet(self.x, self.y, self.direction())
                    self.bullets.append(bullet)
                    self.cool_down_count = 1
                for bullet in self.bullets:
                    bullet.move()
                    if bullet.off_screen():
                        self.bullets.remove(bullet)

            def hit(self):
                for enemy in enemies:
                    for bullet in self.bullets:
                        if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2]:
                            if enemy.hitbox[1] < bullet.y < enemy.hitbox[1] + enemy.hitbox[3]:
                                enemy.health -= self.damage
                                player.bullets.remove(bullet)

            def boost(self):
                win.blit(boost_img, (400, 270))


        class Bullet:
            def __init__(self, x, y, direction):
                self.x = x + 15
                self.y = y + 25
                self.direction = direction

            def draw_bullet(self):
                win.blit(bullet_img, (self.x, self.y))

            def move(self):
                if self.direction == 1:
                    self.x += 20
                if self.direction == -1:
                    self.x -= 20

            def off_screen(self):
                return not (0 <= self.x <= win_width)


        class Enemy:
            def __init__(self, x, y, direction, speed):
                self.x = x
                self.y = y
                self.stepIndex = 0
                self.direction = direction
                self.hitbox = (self.x, self.y, 50, 50)
                self.health = 30
                self.speed = speed

            def step(self):
                if self.stepIndex >= 33:
                    self.stepIndex = 0

            def draw(self, win):
                self.hitbox = (self.x, self.y, 30, 60)
                pygame.draw.rect(win, red, (self.x, self.y - 10, 30, 10))
                if self.health >= 0:
                    pygame.draw.rect(win, green, (self.x, self.y - 10, self.health, 10))

                self.step()
                if self.direction == left:
                    win.blit(enemy_left[self.stepIndex // 3], (self.x, self.y))
                    self.stepIndex += 1
                if self.direction == right:
                    win.blit(enemy_right[self.stepIndex // 3], (self.x, self.y))
                    self.stepIndex += 1

            def move(self):
                self.hit()
                if self.direction == left:
                    self.x -= speed
                if self.direction == right:
                    self.x += speed

            def hit(self):
                if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2]:
                    if player.hitbox[1] < enemy.y + 32 < player.hitbox[1] + player.hitbox[3]:
                        if player.health > 0:
                            player.health -= 10
                            if player.health == 0 and player.lives > 0:
                                player.lives -= 1
                                player.health = 30
                            elif player.health == 0 and player.lives == 0:
                                player.alive = False

            def off_screen(self):
                return not(0 <= self.x <= win_width)


        def boost():
            global tower_health, speed, kill, boost_с
            if boost_с == 1:
                if not (400 >= player.x >= 350):
                    player.boost()
                else:
                    boost_с = 0
                    random3 = random.randint(0, 3)
                    random4 = random.randint(0, 1)
                    if random4 == 0:
                        if random3 == 0:
                            player.damage += 0.4
                        if random3 == 1:
                            player.velx += 0.5
                        if random3 == 2:
                            player.lives += 1
                        if random3 == 3:
                            tower_health += 1
                    if random4 == 1:
                        if random3 == 0:
                            player.damage -= 0.7
                        if random3 == 1:
                            player.velx -= 2
                        if random3 == 2:
                            player.lives -= 1
                        if random3 == 3:
                            tower_health -= 1

        def draw_game():
            global tower_health, speed, kill, boost_с
            win.fill((0, 0, 0))
            win.blit(background, (0, 0))
            win.blit(tower, (340, 90))
            boost()

            # экран

            player.draw(win)
            for bullet in player.bullets:
                bullet.draw_bullet()
            for enemy in enemies:
                enemy.draw(win)

            if not player.alive:
                win.fill((0, 0, 0))
                enemies.remove(enemy)
                font = pygame.font.Font('freesansbold.ttf', 32)
                text1 = font.render('Вы погибли, нажмите R чтобы начать заново', True, white)
                text2 = font.render('Всего убийств:  ' + str(kill), True, white)
                textRect1 = text1.get_rect()
                textRect2 = text2.get_rect()
                textRect1.center = (win_width//2, win_height//2)
                textRect2.center = (win_width//2, win_height//2 + 30)
                win.blit(text1, textRect1)
                win.blit(text2, textRect2)
                if key[pygame.K_r]:
                    player.alive = True
                    player.lives = 2
                    player.health = 30
                    tower_health = 3
                    speed = 0.5
                    kill = 0
            if player.alive:
                font = pygame.font.Font('freesansbold.ttf', 32)
                text1 = font.render('жизней: ' + str(player.lives), True, white)
                text2 = font.render('убийства: ' + str(kill), True, white)
                text3 = font.render('башня: ' + str(tower_health), True, white)
                win.blit(text1, (15, 20))
                win.blit(text2, (200, 20))
                win.blit(text3, (410, 19))

            pygame.time.delay(30)
            pygame.display.update()

        player = Hero(380, 240)
        enemies = []
        speed = 0.3
        tower_health = 3
        kill = 0
        boost_с = 2
        max_speed = 5.2

        # основной цикл
        run = True
        while run:
            # выход из игры
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    run2 = False

            key = pygame.key.get_pressed()

            player.shoot()

            player.move_hero(key)
            player.jump_motion(key)

            if tower_health == 0:
                player.alive = False

            if len(enemies) == 0:
                random1 = random.randint(0, 1)
                random2 = random.randint(0, 4)
                if random2 >= 5:
                    boost_с = 0

                if random2 == 4:
                    boost_с = 1

                if random1 == 1:
                    enemy = Enemy(800, 240, left, speed)
                    enemies.append(enemy)
                    c = 1
                if random1 == 0:
                    enemy = Enemy(0, 240, right, speed)
                    enemies.append(enemy)
                    c = 0
                if speed <= max_speed:
                    speed += 0.45

            for enemy in enemies:
                enemy.move()
                if enemy.off_screen() or enemy.health <= 0:
                    enemies.remove(enemy)
                if c == 1:
                    if enemy.x < 400:
                        enemies.remove(enemy)
                        tower_health -= 1
                if c == 0:
                    if enemy.x > 400:
                        enemies.remove(enemy)
                        tower_health -= 1
                if enemy.health <= 0:
                    kill += 1

            draw_game()

