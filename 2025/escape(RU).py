# Escape — Приключение на Python
# Автор: Шон Макманус / www.sean.co.uk
# Арт: Рафаэль Пимента
# Набрано вручную: УКАЖИТЕ ВАШЕ ИМЯ ЗДЕСЬ

import time, random, math, pgzrun

##################
## ПЕРЕМЕННЫЕ ##
##################

WIDTH = 800 #размер окна игры
HEIGHT = 800

#Переменные игрока
PLAYER_NAME = "Виктор" #измените это на ваше имя!
FRIEND1_NAME = "Саша" #измените это на имя друга!
FRIEND2_NAME = "Лео" #измените это на другое имя друга!
current_room = 31 #начальная комната = 31

top_left_x = 100
top_left_y = 150

DEMO_OBJECTS = [images.floor, images.pillar, images.soil]

LANDER_SECTOR = random.randint(1, 24)
LANDER_X = random.randint(2, 11)
LANDER_Y = random.randint(2, 11)

TILE_SIZE = 30

player_y, player_x = 2, 5
game_over = False

PLAYER = {
    "left": [images.spacesuit_left, images.spacesuit_left_1,
             images.spacesuit_left_2, images.spacesuit_left_3,
             images.spacesuit_left_4
             ],
    "right": [images.spacesuit_right, images.spacesuit_right_1,
              images.spacesuit_right_2, images.spacesuit_right_3,
              images.spacesuit_right_4
              ],
    "up": [images.spacesuit_back, images.spacesuit_back_1,
           images.spacesuit_back_2, images.spacesuit_back_3,
           images.spacesuit_back_4
           ],
    "down": [images.spacesuit_front, images.spacesuit_front_1,
             images.spacesuit_front_2, images.spacesuit_front_3,
             images.spacesuit_front_4
             ]
    }

player_direction = "down"
player_frame = 0
player_image = PLAYER[player_direction][player_frame]
player_offset_x, player_offset_y = 0, 0

PLAYER_SHADOW = {
    "left": [images.spacesuit_left_shadow, images.spacesuit_left_1_shadow,
             images.spacesuit_left_2_shadow, images.spacesuit_left_3_shadow,
             images.spacesuit_left_4_shadow
             ],
    "right": [images.spacesuit_right_shadow, images.spacesuit_right_1_shadow,
              images.spacesuit_right_2_shadow,
              images.spacesuit_right_3_shadow, images.spacesuit_right_4_shadow
              ],
    "up": [images.spacesuit_back_shadow, images.spacesuit_back_1_shadow,
           images.spacesuit_back_2_shadow, images.spacesuit_back_3_shadow,
           images.spacesuit_back_4_shadow
           ],
    "down": [images.spacesuit_front_shadow, images.spacesuit_front_1_shadow,
             images.spacesuit_front_2_shadow, images.spacesuit_front_3_shadow,
             images.spacesuit_front_4_shadow
             ]
    }

player_image_shadow = PLAYER_SHADOW["down"][0]

PILLARS = [
    images.pillar, images.pillar_95, images.pillar_80,
    images.pillar_60, images.pillar_50
    ]

wall_transparency_frame = 0

BLACK = (0, 0, 0)
BLUE = (0, 155, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (128, 0, 0)

air, energy = 100, 100
suit_stitched, air_fixed = False, False
launch_frame = 0


#################
##   КАРТА     ##
#################

MAP_WIDTH = 5
MAP_HEIGHT = 10
MAP_SIZE = MAP_WIDTH * MAP_HEIGHT

GAME_MAP = [ ["Комната 0 - где хранятся неиспользуемые объекты", 0, 0, False, False] ]

outdoor_rooms = range(1, 26)
for planetsectors in range(1, 26): #комнаты от 1 до 25 генерируются здесь
    GAME_MAP.append( ["Поверхность пыльной планеты", 13, 13, True, True] )

GAME_MAP  += [
        #["Название комнаты", высота, ширина, Верхний выход?, Правый выход?]
        ["Воздушный шлюз", 13, 5, True, False], # комната 26
        ["Лаборатория инженерии", 13, 13, False, False], # комната 27
        ["Центр управления миссией пуделей", 9, 13, False, True], # комната 28
        ["Галерея обзора", 9, 15, False, False], # комната 29
        ["Санузел экипажа", 5, 5, False, False], # комната 30
        ["Зал воздушного шлюза", 7, 11, True, True], # комната 31
        ["Левая комната для перемещения", 9, 7, True, False], # комната 32
        ["Правая комната для перемещения", 7, 13, True, True], # комната 33
        ["Научная лаборатория", 13, 13, False, True], # комната 34






















#################
##   ОБЪЕКТЫ   ##
#################

objects = {
    0: [images.floor, None, "Пол блестящий и чистый"],
    1: [images.pillar, images.full_shadow, "Стена гладкая и холодная"],
    2: [images.soil, None, "Похоже на пустыню. Или десерт?"],
    3: [images.pillar_low, images.half_shadow, "Стена гладкая и холодная"],
    4: [images.bed, images.half_shadow, "Аккуратная и удобная кровать"],
    5: [images.table, images.half_shadow, "Сделан из прочного пластика."],
    6: [images.chair_left, None, "Кресло с мягкой подушкой"],
    7: [images.chair_right, None, "Кресло с мягкой подушкой"],
    8: [images.bookcase_tall, images.full_shadow,
        "Высокие книжные полки, заполненные справочниками"],
    9: [images.bookcase_small, images.half_shadow,
        "Маленькие книжные полки, заполненные справочниками"],
    10: [images.cabinet, images.half_shadow,
         "Небольшой шкафчик для хранения личных вещей"],
    11: [images.desk_computer, images.half_shadow,
         "Компьютер. Используйте его для диагностики жизнеобеспечения"],
    12: [images.plant, images.plant_shadow, "Растение пространберри, выращенное здесь"],
    13: [images.electrical1, images.half_shadow,
         "Электрические системы для питания космической станции"],
    14: [images.electrical2, images.half_shadow,
         "Электрические системы для питания космической станции"],
    15: [images.cactus, images.cactus_shadow, "Остерегайтесь кактуса! Осторожнее!"],
    16: [images.shrub, images.shrub_shadow,
         "Космический салат. Немного вял, но удивительно, что растет здесь!"],
    17: [images.pipes1, images.pipes1_shadow, "Трубы очистки воды"],
    18: [images.pipes2, images.pipes2_shadow,
         "Трубы для систем жизнеобеспечения"],
    19: [images.pipes3, images.pipes3_shadow,
         "Трубы для систем жизнеобеспечения"],
    20: [images.door, images.door_shadow, "Безопасная дверь. Открывается автоматически\
    для астронавтов в исправных скафандрах."],
    21: [images.door, images.door_shadow, "Дверь воздушного шлюза.\
    По соображениям безопасности требует двух человек для открытия."],
    22: [images.door, images.door_shadow, "Закрытая дверь. Требуется"\ "карта доступа " + PLAYER_NAME],
    23: [images.door, images.door_shadow, "Закрытая дверь. Требуется" "карта доступа " + FRIEND1_NAME],
    24: [images.door, images.door_shadow, "Закрытая дверь. Требуется" "карта доступа " + FRIEND2_NAME],
    25: [images.door, images.door_shadow,
         "Закрытая дверь. Она открывается из Главного центра управления миссией"],
    26: [images.door, images.door_shadow,
         "Закрытая дверь в инженерном отсеке."],
    27: [images.map, images.full_shadow,
         "Экран показывает местоположение крушения было сектор: " \
         + str(LANDER_SECTOR) + " // Х: " + str(LANDER_X) + \
         " // Y: " + str(LANDER_Y)],
    28: [images.rock_large, images.rock_large_shadow,
         "Камень. Его грубая поверхность похожа на точильный камень", "камень"],
    29: [images.rock_small, images.rock_small_shadow,
         "Небольшой, но тяжелый кусок марсианской породы"],
    30: [images.crater, None, "Кратер на поверхности планеты"],
    31: [images.fence, None,
         "Тончайшая сетка забора. Помогает защитить станцию от пылевых бурь"],
    32: [images.contraption, images.contraption_shadow,
         "Один из научных экспериментов. Легко вибрирует"],
    33: [images.robot_arm, images.robot_arm_shadow,
         "Роботизированная рука, используемая для подъема тяжестей"],
    34: [images.toilet, images.half_shadow, "Искрящийся чистый туалет"],
    35: [images.sink, None, "Раковина с проточной водой", "краны"],
    36: [images.globe, images.globe_shadow,
         "Огромный глобус планеты. Внутри мягко светится"],
    37: [images.science_lab_table, None,
         "Экспериментальный стол, анализирующий почву и пыль планеты"],
    38: [images.vending_machine, images.full_shadow,
         "Автомат с напитками. Нужна кредитка.", "автомат с напитками"],














































 63: [0, 0, 0],
    64: [27, 8, 3], 65: [50, 1, 7], 66: [39, 5, 6], 67: [46, 1, 1],
    68: [0, 0, 0], 69: [30, 3, 3], 70: [47, 1, 3],
    71: [0, LANDER_Y, LANDER_X], 72: [0, 0, 0], 73: [27, 4, 6],
    74: [28, 1, 11], 75: [0, 0, 0], 76: [41, 3, 5], 77: [0, 0, 0],
    78: [35, 9, 11], 79: [26, 3, 2], 80: [41, 7, 5], 81: [29, 1, 1]
    }

checksum = 0
for key, prop in props.items():
    if key != 71: # Объект 71 пропускается, потому что он различается каждый раз.
        checksum += (prop[0] * key
                     + prop[1] * (key + 1)
                     + prop[2] * (key + 2))
print(len(props), "элементов")
assert len(props) == 37, "Ожидается 37 элементов инвентаря"
print("Контрольная сумма элементов:", checksum)
assert checksum == 61414, "Ошибка в данных элементов"


in_my_pockets = [55]
selected_item = 0 # первый элемент
item_carrying = in_my_pockets[selected_item]

RECIPES = [
    [62, 35, 63], [76, 28, 77], [78, 38, 54], [73, 74, 75],
    [59, 54, 60], [77, 55, 56], [56, 57, 58], [71, 65, 72],
    [88, 58, 89], [89, 60, 90], [67, 35, 68]
    ]

checksum = 0
check_counter = 1
for recipe in RECIPES:
    checksum += (recipe[0] * check_counter
                 + recipe[1] * (check_counter + 1)
                 + recipe[2] * (check_counter + 2))
    check_counter += 3
print(len(RECIPES), "рецептов")
assert len(RECIPES) == 11, "Ожидается 11 рецептов"
assert checksum == 37296, "Ошибка в данных рецептов"
print("Контрольная сумма рецепта:", checksum)


############################
## ВЗАИМОДЕЙСТВИЕ С ЭЛЕМЕНТАМИ ##
############################

def find_object_start_x():
    checker_x = player_x
    while room_map[player_y][checker_x] == 255:
        checker_x -= 1
    return checker_x

def get_item_under_player():
    item_x = find_object_start_x()
    item_player_is_on = room_map[player_y][item_x]
    return item_player_is_on

def pick_up_object():
    global room_map
    # Получаем номер объекта в положении игрока.
    item_player_is_on = get_item_under_player()
    if item_player_is_on in items_player_may_carry:
        # Освобождаем пространство на полу.
        room_map[player_y][player_x] = get_floor_type()
        add_object(item_player_is_on)
        show_text("Сейчас несёте " + objects[item_player_is_on][3], 0)
        sounds.pickup.play()
        time.sleep(0.5)
    else:
        show_text("Нельзя нести этот предмет!", 0)

def add_object(item): # добавляет предмет в инвентарь.
    global selected_item, item_carrying
    in_my_pockets.append(item)
    item_carrying = item
    # Минус единица, поскольку индексы начинаются с нуля.
    selected_item = len(in_my_pockets) - 1
    display_inventory()
    props[item][0] = 0 # Предметы, находящиеся в руках, переносятся в комнату 0 (вне карты).

def display_inventory():
    box = Rect((0, 45), (800, 105))
    screen.draw.filled_rect(box, BLACK)

    if len(in_my_pockets) == 0:
        return

    start_display = (selected_item // 16) * 16
    list_to_show = in_my_pockets[start_display : start_display + 16]
    selected_marker = selected_item % 16

    for item_counter in range(len(list_to_show)):
        item_number = list_to_show[item_counter]
        image = objects[item_number][0]
        screen.blit(image, (25 + (46 * item_counter), 90))

    box_left = (selected_marker * 46) - 3
    box = Rect((22 + box_left, 85), (40, 40))
    screen.draw.rect(box, WHITE)
    item_highlighted = in_my_pockets[selected_item]
    description = objects[item_highlighted][2]
    screen.draw.text(description, (20, 130), color="white")

def drop_object(old_y, old_x):
    global room_map, props
    if room_map[old_y][old_x] in [0, 2, 39]: #места, куда можно положить вещи
        props[item_carrying][0] = current_room
        props[item_carrying][1] = old_y
        props[item_carrying][2] = old_x
        room_map[old_y][old_x] = item_carrying
        show_text("Вы бросили " + objects[item_carrying][3], 0)
        sounds.drop.play()
        remove_ob...

pgzrun.go()