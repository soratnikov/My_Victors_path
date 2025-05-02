import pygame, os, random

'''
Переменные
'''
BOARD_X = 600 # Константы принято именовать КАПСОМ, так питонисты намекают друг другу что это не стоит менять:)
BOARD_Y = 600 # эти две полезно использовать при проверке границ мира, строка 125
fps = 40
main = True
anima = 4 #название получше  надо
size = 45

SPEED = [2,2]

def enemy_loc():
    return random.randint(10, 550)


'''
Объекты
'''
class Pacman(pygame.sprite.Sprite):
    #pac-man:
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

        # self.rect.x = self.rect.x + self.movex
        # self.rect.y = self.rect.y + self.movey
        self.rect.x += self.movex
        self.rect.y += self.movey

        #влево:
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3*anima:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame//anima], True, False)
            # print('self.frameLEFT=', self.frame)
        #вправо:
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*anima:
                self.frame = 0
            self.image = self.images[self.frame//anima]
            # print('self.frameRIGHT=', self.frame)
        #вверх:
        if self.movey < 0:
            self.frame += 1
            if self.frame > 3*anima:
                self.frame = 0
            self.image = pygame.transform.rotate(self.images[self.frame//anima], 90)
            # print('self.frameUP=', self.frame)

        #вниз:
        if self.movey > 0:
            self.frame += 1
            if self.frame > 3*anima:
                self.frame = 0
            self.image = pygame.transform.rotate(self.images[self.frame//anima], -90)
            # print('self.frameDOWN=', self.frame)





    def overmove(self):
        if self.rect.x > 550:
            self.steps = -10



class Enemy(pygame.sprite.Sprite):
    #enemy:
    def __init__(self, name, addnumber, speed = [2,2] ):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('Images', f'{name}.png')).convert_alpha()
            self.images.append(pygame.transform.scale(img, (size, size)))
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = enemy_loc()
            self.rect.y = enemy_loc()
            self.speed = speed
            self.name = name
            self.addnumber = addnumber

    def rand_vec(self):
        return random.randint(-1, 1)

    def move(self):
        #перемещение спрайта приведений:

        r =self.rect
        r.top # Удобнее
        r.bottom # Удобнее
        r.left # Удобнее
        r.right # Удобнее
        
        r.x = r.x + self.speed[0]
        r.y = r.y + self.speed[1]

        if r.left < 0 or r.right > BOARD_X: # Так читается проще, на мой взгляд
            self.speed[0] *= -1
        if (r.y < 0) or (r.y > 600-60):
            self.speed[1] *= -1



        

    def update(self):
        #обновление позиции спрайта

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

    def enemy_rect_x(self):
        return int(random.uniform(10, 550))

    def enemy_rect_y(self):
        return int(random.uniform(10, 550))

    def overmove(self):
        if self.rect.y > 200:
            print("oops!")

    def get_name(self):
        return self.name






'''
Настройка
'''
clock = pygame.time.Clock()
pygame.init()
board = pygame.display.set_mode([BOARD_X, BOARD_Y])
bg_img = pygame.image.load(os.path.join('Images', '600-600.jpg'))

boardbox = board.get_rect()
pac_man = Pacman()
pac_man.rect.x = 300-(size/2)
pac_man.rect.y = 300-(size/2)

pac_man_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
pac_man_list.add(pac_man)


enemy_1 = Enemy("blue", 120)
enemy_2 = Enemy("orange", 100)
enemy_3 = Enemy("pink", 16)
enemy_4 = Enemy("red", 8)


enemy_list.add(enemy_1) 
enemy_list.add(enemy_2)
enemy_list.add(enemy_3)
enemy_list.add(enemy_4)


steps = 3

'''
Игровой цикл
'''



while main:
    #Для проверки зажатия лучше использовать:
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_любая_клавиша]:
    #     pac_man.move(-steps, 0)
        # в этом случае постоянное движение проще кодируется

    for event in pygame.event.get(): # Эта конструкция для одноразовых событий, типо прыжков.



        if event.type == pygame.QUIT:
            pygame.quit()


        keys = pygame.key.get_pressed()


        if keys[pygame.K_LEFT]:
            pac_man.move(-steps, 0)

        if keys[pygame.K_RIGHT]:
            pac_man.move(steps, 0)

        if keys[pygame.K_UP]:
            pac_man.move(0, -steps)

        if keys[pygame.K_DOWN]:
            pac_man.move(0, steps)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pac_man.move(steps, 0)
            elif event.key == pygame.K_RIGHT:
                pac_man.move(-steps, 0)
            elif event.key == pygame.K_UP:
                pac_man.move(0, steps)
            elif event.key == pygame.K_DOWN:
                pac_man.move(0, -steps)
            pac_man.overmove()
    pac_man.rect.clamp_ip(boardbox)  # Pacman останавливается при столкновении со стеной


    board.blit(bg_img, boardbox)
    pac_man.update() # название не отражает сути.
    pac_man_list.draw(board)
    enemy_list.draw(board)
    for i in enemy_list:
        i.move()
    hits = pygame.sprite.spritecollide(pac_man, enemy_list, True)
    if hits:
        # print('I eat something', 'XXXX', 'monster', enemy_list.sprites())
        print(hits[0]) # <EnemySprite ( in 0 groups)>
    pygame.display.update()
    if not len(enemy_list): # not 0 == True == 1
        print('RELOAD')
    clock.tick(fps)
