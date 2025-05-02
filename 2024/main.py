# light pac-man

import os
import numpy as np
import pygame
import random

'''
Переменные и константы
'''
BOARD_X = 600
BOARD_Y = 600
fps = 80
main = True
ani = 4
size = 45
addx = 1
addy = 1
f = 10

'''
Объекты
'''


class Pacman(pygame.sprite.Sprite):
    #Класс с Pacman:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('Images', f'{i}.png')).convert_alpha()
            self.images.append(pygame.transform.scale(img, (size, size)))
            self.image = self.images[0]
            self.rect = self.image.get_rect()
        self.movex = 0
        self.movey = 0
        self.frame = 1

    def move(self, x, y):
        #перемещение спрайта:
        self.movex += x
        self.movey += y

    def update(self):
        #обновление позиции спрайта

        self.rect.x += self.movex
        self.rect.y += self.movey

        self.position = 0

        #влево:
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)
            self.position = 2
            # print('self.frameLEFT=', self.frame, self.position)
        #вправо:
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani]
            self.position = 0
            # print('self.frameRIGHT=', self.frame, self.position)

        #вверх:
        if self.movey < 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = pygame.transform.rotate(self.images[self.frame // ani], 90)
            self.position = 1
            # print('self.frameUP=', self.frame, self.position)
        #вниз:
        if self.movey > 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = pygame.transform.rotate(self.images[self.frame // ani], -90)
            self.position = 3
            # print('self.frameDOWN=', self.frame, self.position)


class Enemy(pygame.sprite.Sprite):
    #класс с привидениями:
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        img = pygame.image.load(os.path.join('Images', f'{name}.png')).convert_alpha()
        self.images.append(pygame.transform.scale(img, (size, size)))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        r = self.rect
        self.name = name
        r.x = random.randrange(0, 500)
        r.y = random.randrange(0, 500)
        self.addx = addx
        self.addy = addy
        self.speedy = random.randrange(1, 4)  #движение в случайном направлении
        self.speedx = random.randrange(-3, 1)
        self.timeout = timeout

    def update(self, timeout, addx, addy):
        #Перемещение спрайта привидений:

        r = self.rect
        r.x += self.speedx * self.addx
        r.y += self.speedy * self.addy

        #Ограничение игрового поля для приведений и изменение вектора скорости каждые 5 секунд
        bump_kill = False
        pac_man_bump = pygame.sprite.groupcollide(pac_man_list, enemy_list, bump_kill, True)



        if ((r.left < 1) or (r.right > BOARD_X - 2)) \
            or pac_man.position == 1 and pac_man_bump \
            or pac_man.position == 2 and pac_man_bump \
            or pac_man.position == 3 and pac_man_bump:
                self.speedx *= -1

        if ((r.top < 1) or (r.bottom > BOARD_Y - 2)) \
            or pac_man.position == 1 and pac_man_bump \
            or pac_man.position == 2 and pac_man_bump \
            or pac_man.position == 3 and pac_man_bump:
                self.speedy *= -1


        if pac_man.position == 0 and pac_man_bump:
            bump_kill == True
            self.speedx *= -1
            self.speedy *= -1


        # if timeout // 5:
        #     self.addx = np.sin((2 * np.pi * f) / 100 * timeout)

        #x = A*sin(w*t), где w = 2*pi*f/fd, A - амплитуда волны - формула из радиотехники :)



        # if timeout // 5:
        #     self.addy = np.sin((2 * np.pi * f) / 100 * timeout)






    def get_name(self):
        # return self.name
        print (self.name)


'''
Настройка
'''
clock = pygame.time.Clock()
pygame.init()
board = pygame.display.set_mode([BOARD_X, BOARD_Y])
bg_img = pygame.image.load(os.path.join('Images', '600-600.jpg'))

boardbox = board.get_rect()
pac_man = Pacman()
pac_man.rect.x = BOARD_X / 2 - size / 2  #Pacman появляется в центре игрового поля
pac_man.rect.y = BOARD_Y / 2 - size / 2
enemy_list = pygame.sprite.Group()
pac_man_list = pygame.sprite.Group()
pac_man_list.add(pac_man)
reset_time = 1
kill = True

myfont = pygame.font.Font('Fonts/Jersey10Charted-Regular.ttf', 100)


def add_enemys():
    names = ['blue', 'orange', 'pink', 'red']
    for i, name in enumerate(names):
        e = Enemy(name)
        enemy_list.add(e)
        # print(e.name)

steps = 3

'''
Игровой цикл
'''

while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        #Управление Pacman, клавиша нажата
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pac_man.move(-steps, 0)
            if event.key == pygame.K_RIGHT:
                pac_man.move(steps, 0)
            elif event.key == pygame.K_UP:
                pac_man.move(0, -steps)
            elif event.key == pygame.K_DOWN:
                pac_man.move(0, steps)

        #Управление Pacman, клавиша отжата
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pac_man.move(steps, 0)
            elif event.key == pygame.K_RIGHT:
                pac_man.move(-steps, 0)
            elif event.key == pygame.K_UP:
                pac_man.move(0, steps)
            elif event.key == pygame.K_DOWN:
                pac_man.move(0, -steps)

    timeout = int((pygame.time.get_ticks() / 1000))  #прошло времени в секундах

    # print(timeout)
    text_surface_time = myfont.render(str(timeout), True, 'White')
    pac_man.rect.clamp_ip(boardbox)  #Pacman останавливается при столкновении со стеной
    board.blit(bg_img, boardbox)
    board.blit(text_surface_time, (15, 15))
    pac_man_list.update()
    pac_man_list.draw(board)
    enemy_list.draw(board)

    for s in enemy_list:
        t = random.uniform(0, 300)
    #
        print(s.name)
    #
    #
        # pac_man_bump = pygame.sprite.spritecollide(pac_man, enemy_list, False)
    #
    #     if pac_man.position == (1 and pac_man_bump) or (2 and pac_man_bump) or (3 and pac_man_bump):
    #         s.speedx += -1
    #         s.speedy += -1
    #
    #         for i in range(2):
    #             print("goal!")

        # if pac_man.position == 0:
        #     kill = True
        #     hit_kill = pygame.sprite.spritecollide(pac_man, enemy_list, kill)  #проверка столкновения
        #     if hit_kill:
        #         for enemy in enemy_list.sprites():
        #             print(enemy.name)
        #         # print(f'I eat {enemy_list[i].name} something monster')
                # print(enemy.name)
        # else:
        #     pass
        s.update(timeout, addx, addy)

    pygame.display.update()
    if not len(enemy_list):  #все враги съедены, добавляются новые
        add_enemys()
    clock.tick(fps)
