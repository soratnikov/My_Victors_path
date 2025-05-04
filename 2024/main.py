# light pac-man all done

import os
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
eated_ghost = ["Pacman is hungry"]

'''
Объекты
'''
pygame.init()
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

        #Ограничение игрового поля для приведений и изменение вектора скорости при столкновении
        pac_man_bump = pygame.sprite.groupcollide(pac_man_list, enemy_list, False, False)

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
            self.speedx *= -1
            self.speedy *= -1

        # Если произошло столкновение между Пакманом и врагом
        if len(pac_man_bump) > 0:
            for key in pac_man_bump.keys():
                # Получаем список привидений, с которыми столкнулся Пакман
                enemies_collided = pac_man_bump[key]

                # Проверяем каждый объект-привидение
                for enemy in enemies_collided:
                    global eated_ghost
                    # Здесь получаем имя привидения, которое схватил Пакман
                    eated_ghost.append(enemy.name)
                    # print(f"Пакман съел {enemy.name}")

                    # Теперь можно удалить привидение
                    enemy.kill()



                        # if timeout // 5:
        #     self.addx = np.sin((2 * np.pi * f) / 100 * timeout)

        #x = A*sin(w*t), где w = 2*pi*f/fd, A - амплитуда волны - формула из радиотехники :)

        # if timeout // 5:
        #     self.addy = np.sin((2 * np.pi * f) / 100 * timeout)

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

myfont = pygame.font.Font('Fonts/Jersey10Charted-Regular.ttf', 84)

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

    text_surface_time = myfont.render(str(timeout), True, 'White')

    if len(eated_ghost) > 1:
        color_ghost = str(eated_ghost[-1])
        print(color_ghost)
    else:
        color_ghost = "brown"
    eated_ghost_text_surface = myfont.render(f'Pacman ate: {str(eated_ghost[-1])}', True, color_ghost)

    pac_man.rect.clamp_ip(boardbox) #Pacman останавливается при столкновении со стеной
    board.blit(bg_img, boardbox)
    board.blit(eated_ghost_text_surface, (15, 120))
    board.blit(text_surface_time, (15, 15))
    pac_man_list.update()
    pac_man_list.draw(board)
    enemy_list.draw(board)

    for s in enemy_list:
        t = random.uniform(0, 300)
        s.update(timeout, addx, addy)


# вариант, предложенный ИИ
    collisions = []
    for sprite1 in enemy_list.sprites():
        for sprite2 in enemy_list.sprites():
            if sprite1 != sprite2 and pygame.sprite.collide_rect(sprite1, sprite2):
                collisions.append((sprite1, sprite2))

    # Обрабатываем столкновения
    for collided_pair in collisions:
        ghost1, ghost2 = collided_pair
        # Тут можно задать поведение при столкновении,
        # например, поменять направление движения одного из привидений
        ghost1.update(0.1, -1, 1)
        ghost2.update(0.1, 1, 1)






    pygame.display.update()
    if not len(enemy_list):  #все враги съедены, добавляются новые, счетчик съеденных обнуляется
        eated_ghost = ["Pacman is hungry!"]
        add_enemys()
    clock.tick(fps)