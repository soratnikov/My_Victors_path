
#I Want become your father

import random, pygame



clock = pygame.time.Clock()
pygame.init()

screen_h = 460
screen_w = 819
i = 1

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("pygame_Victors_path")
icon = pygame.image.load('images/ico.png')
pygame.display.set_icon(icon)
t = 3
player = pygame.image.load(f'images/{i}.png').convert_alpha()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1,4):
            img = pygame.image.load(f'images/{i}.png').convert_alpha()
            self.images.append(img)
            self.image = self.images[i]
            self.rect = self.image.get_rect()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1,4):
            img = pygame.image.load(f'images/{i}.png').convert_alpha()
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

BG_background = pygame.image.load('images/desert_BG_size.jpg').convert()
player_anim_count = 0
player_anim_count_shoot = 0
enemy_anim_count = 0
sprite_images = []
sprite_sheet = pygame.image.load('images/hand-sprite-sheet.png').convert_alpha()

sprite_rect_x = 70
sprite_rect_y = 60
shift_x = 0
shift_y = 0
count_x = 0
count_y = 0
bg_x = 0
player_speed = 20
player_x = 150
player_y = 20

enemy_speed = 20
enemy_x = 650
# enemy_y = 300
enemy_y = random.randint(0, 300)

bullets = []

#bg_sound = pygame.mixer.Sound('Sound/kubbi.mp3')
#bg_sound.play(-1)

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 5000)

label = pygame.font.Font("fonts/Jersey10Charted-Regular.ttf", 60)
lose_label = label.render("GAME OVER!", False, (193, 196, 199))
restart_label = label.render("RESTART", False, (115, 130, 199))
restart_label_hitbox = restart_label.get_rect(topleft=(320, 230))
bullets_lef = 5

playgame = True

myfont = pygame.font.Font('fonts/Jersey10Charted-Regular.ttf', 60)
text_surface_victor = myfont.render('Victor, I want become your father', True, 'Orange')
text_surface_coord_x = myfont.render(str(player_x), True, 'Orange')
text_surface_coord_y = myfont.render(str(player_y), True, 'Orange')

enemy_list_in_game = []

"""Skanirovanie spraita"""

for i in range(5):
    for j in range(8):
        sprite_rect = pygame.Rect(shift_x, shift_y, 70, 60)
        sprite_images.append(sprite_sheet.subsurface(sprite_rect))
        shift_x += 70
        # print(len(sprite_images), " ", shift_x, " ", shift_y)

    shift_x = 0
    shift_y += 70
    print(len(sprite_images), " ", shift_x, " ", shift_y)
print("ПОлное количество спрайтов: ", len(sprite_images))

'''Polzovatelskie funkcii'''


def flipp(self):
    return pygame.transform.flip(self, flip_x=1, flip_y=0)


def squashh(self, a, b):
    return pygame.transform.scale(self, (sprite_rect_x * a, sprite_rect_y * b))


bullet = squashh(flipp(sprite_images[28]), 1.5, 1.5)

'''Hranilische spraitov'''

hand_move_left = []
for i in range(len(sprite_images)):
    hand_move_left.append(sprite_images[i])
    # print(hand_move_left)

hand_move_right = []
for i in range(len(sprite_images)):
    hand_move_right.append(flipp(sprite_images[i]))
    # print(hand_move_right)

player_hand = []
for i in range(24, 29):
    player_hand.append(sprite_images[i])

enemy_hand = []
for i in range(0, 8):
    enemy_hand.append(sprite_images[i])

"""Osnovnoy cikl"""

running = True
while running:

    screen.blit(BG_background, (bg_x, 0))
    screen.blit(BG_background, (bg_x + 819, 0))
    screen.blit(bullet, (150, 150))

    if playgame:
        bg_x -= 9
        if bg_x == -819:
            bg_x = 0

        player_hitbox = squashh(sprite_images[26], 1.5, 1.5).get_rect(topleft=(player_x, player_y))

        if enemy_anim_count == 6:
            enemy_anim_count = 0
        else:
            enemy_anim_count += 1

        if enemy_list_in_game:
            for (i, el) in enumerate(enemy_list_in_game):
                if el.x > 0:
                    screen.blit(squashh(enemy_hand[enemy_anim_count], 1.5, 1.5), (el.x, el.y))
                    el.x -= 10
                else:
                    el.x = 700
                    el.y = random.randint(0, 300)
                    enemy_list_in_game.pop(i)

                if player_hitbox.colliderect(el):
                    playgame = False

            text_surface_coord_x = myfont.render(str(el.x), True, 'Orange')
            text_surface_coord_y = myfont.render(str(el.y), True, 'Orange')

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and keys[pygame.K_a]:
            player_x -= player_speed * 10
        elif keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        elif keys[pygame.K_DOWN] and player_y < 360:
            player_y += player_speed
        elif keys[pygame.K_RIGHT] and player_x < 730:
            player_x += player_speed
        elif keys[pygame.K_LEFT] and player_x > 5:
            player_x -= player_speed

        screen.blit(text_surface_victor, (50, 15))
        screen.blit(text_surface_coord_x, (50, 150))
        screen.blit(text_surface_coord_y, (50, 200))
        # screen.blit(hand_move_left[25], (640,380))
        # screen.blit(hand_move_left[28], (600,380))

        if player_anim_count == 1:
            pygame.time.wait(10)
            player_anim_count = 0
        else:
            player_anim_count += 1

        if player_anim_count_shoot == 2:
            player_anim_count_shoot = 1
        else:
            player_anim_count_shoot += 1

        if keys[pygame.K_RIGHT]:
            screen.blit(squashh(flipp(player_hand[player_anim_count]), 1.5, 1.5), (player_x, player_y))

        elif keys[pygame.K_LEFT]:
            screen.blit(squashh(player_hand[player_anim_count], 1.5, 1.5), (player_x, player_y))

        else:
            screen.blit(squashh(flipp(player_hand[player_anim_count]), 1.5, 1.5), (player_x, player_y))

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 40

                if el.x > screen_w - 50:
                    bullets.pop(i)

                if enemy_list_in_game:
                    for (index, enemy) in enumerate(enemy_list_in_game):
                        if el.colliderect(enemy):
                            enemy_list_in_game.pop(index)
                            bullets.pop(i)


    else:
        screen.fill((0, 200, 0))
        screen.blit(lose_label, (300, 120))
        screen.blit(restart_label, (320, 230))
        mouse = pygame.mouse.get_pos()
        if restart_label_hitbox.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            playgame = True
            player_x = 50
            enemy_list_in_game.clear()
            bullets.clear()
            bullets_lef = 5

    pygame.display.update()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy_hand[0].get_rect(topleft=(650, 200)))

        if playgame and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_lef > 0:
            screen.blit(squashh(flipp(player_hand[player_anim_count_shoot]), 1.5, 1.5), (player_x, player_y))
            bullets.append(bullet.get_rect(topleft=(player_x + 80, player_y - 15)))
            bullets_lef -= 1

    clock.tick(5)
