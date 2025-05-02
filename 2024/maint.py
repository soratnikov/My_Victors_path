import random, pygame

clock = pygame.time.Clock()
pygame.init()



screen_w = 460
screen_h = 819

screen = pygame.display.set_mode((screen_h, screen_w))
pygame.display.set_caption("pygame_Victors_path")
icon = pygame.image.load('Images/ico.png')
pygame.display.set_icon(icon)
t=3
player = pygame.image.load('Images/ico.png').convert_alpha()
BG_background = pygame.image.load('Images/desert_BG_size.jpg').convert()
player_anim_count = 0
enemy_anim_count = 0
sprite_images = []
sprite_sheet = pygame.image.load('Images/hand-sprite-sheet.png').convert_alpha()

sprite_rect_x = 70
sprite_rect_y = 60
shift_x = 0
shift_y = 0
count_x = 0
count_y = 0
bg_x = 0
bullets = []
player_speed = 20
player_x = 150
player_y = 20

enemy_speed = 20
enemy_x = 650
enemy_y = 300

bg_sound = pygame.mixer.Sound('Sound/kubbi.mp3')
bg_sound.play(-1)

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 5000)

label = pygame.font.Font("Fonts/Jersey10Charted-Regular.ttf", 60)
lose_label = label.render("GAME OVER!", False, (193, 196, 199))
restart_label = label.render("RESTART", False, (115, 130, 199))
restart_label_hitbox = restart_label.get_rect(topleft=(320, 230))


playgame = True

"""Skanirovanie spraita"""

for i in range(5):
    for j in range(8):
         sprite_rect = pygame.Rect(shift_x, shift_y, 70, 60)
         sprite_images.append(sprite_sheet.subsurface(sprite_rect))
         shift_x += 70
         print(len(sprite_images), " ", shift_x, " ", shift_y)
    # sprite_images.append(sprite_images)
    shift_x = 0
    shift_y += 70
    print(len(sprite_images), " ", shift_x, " ", shift_y)
print("ПОлное количество спрайтов: ", len(sprite_images))

myfont = pygame.font.Font('Fonts/Jersey10Charted-Regular.ttf', 60)
text_surface_victor = myfont.render('Victor, I want become your father', True, 'Orange')
text_surface_coord_x = myfont.render(str(player_x), True, 'Orange')
text_surface_coord_y = myfont.render(str(player_y), True, 'Orange')

enemy_list_in_game = []

'''Polzovatelskie funkcii'''

def flipp(self):
    return pygame.transform.flip(self, flip_x = 1, flip_y = 0)

def squashh(self, a,b):
    return pygame.transform.scale(self, (a,b))

'''Hranilische spraitov'''

hand_move_left = []
for i in range(len(sprite_images)):
    hand_move_left.append(sprite_images[i])
    # print(hand_move_left)

hand_move_right = []
for i in range(len(sprite_images)):
    hand_move_right.append(flipp(hand_move_left[i]))
    # print(hand_move_right)



enemy_hand_right = []
for i in range(25,29):
    enemy_hand_right.append(hand_move_left[i])

enemy_y = random.randint(0, 300)


"""Osnovnoy cikl"""


running = True
while running:

    screen.blit(BG_background,(bg_x, 0))
    screen.blit(BG_background,(bg_x+819, 0))

    if playgame:
        bg_x -= 9
        if bg_x == -819:
            bg_x = 0

        player_hitbox = squashh(hand_move_right[0], sprite_rect_x*1.5, sprite_rect_y*1.5).get_rect(topleft=(player_x, player_y))

        if enemy_anim_count == 1:
            enemy_anim_count = 0
        else:
            enemy_anim_count += 1

        if enemy_list_in_game:
            for (i, el) in enumerate(enemy_list_in_game):
                if el.x > 0:
                    screen.blit(squashh(enemy_hand_right[enemy_anim_count], sprite_rect_x * 1.5, sprite_rect_y * 1.5), (el.x, el.y))
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
            player_x -= player_speed*10
        elif keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        elif keys[pygame.K_DOWN] and player_y < 360:
            player_y += player_speed
        elif keys[pygame.K_RIGHT] and player_x < 730 :
            player_x += player_speed
        elif keys[pygame.K_LEFT] and player_x > 5:
            player_x -= player_speed



        screen.blit(text_surface_victor,(50, 15))
        screen.blit(text_surface_coord_x,(50, 150))
        screen.blit(text_surface_coord_y,(50, 200))
        # screen.blit(hand_move_left[25], (640,380))
        # screen.blit(hand_move_left[28], (600,380))



        if player_anim_count == 7:
            player_anim_count = 0
        else:
            player_anim_count += 1







        if keys [pygame.K_RIGHT]:
            screen.blit(squashh(hand_move_right[player_anim_count], sprite_rect_x*1.5, sprite_rect_y*1.5), (player_x,player_y))
        elif keys [pygame.K_LEFT]:
            screen.blit(squashh(hand_move_left[player_anim_count], sprite_rect_x*1.5, sprite_rect_y*1.5), (player_x,player_y))
        else:
            screen.blit(squashh(hand_move_right[player_anim_count], sprite_rect_x*1.5, sprite_rect_y*1.5), (player_x,player_y))






        # cu = 0
        # for image in hand_move_left:
        #    screen.blit(image, (cu*70, 80))
        #    cu += 1
        # cu = 0
        # for image in hand_move_right:
        #    screen.blit(image, (cu*80, 160))
        #    cu += 1
    else:
        screen.fill((0, 200, 0))
        screen.blit(lose_label, (300, 120))
        screen.blit(restart_label, (320, 230))
        mouse = pygame.mouse.get_pos()
        if restart_label_hitbox.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            playgame = True
            player_x = 50
            enemy_list_in_game.clear()

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy_hand_right[2].get_rect(topleft=(650, 200)))

    clock.tick(5)





