# Побег — приключение на Python
# Шон Макманус / www.sean.co.uk
# Иллюстрации Рафаэля Пимента
# Набрано ВАШИМ ИМЕНЕМ ЗДЕСЬ

import time, random, math, pgzrun

from pgzero.clock import clock

from pgzero.keyboard import keyboard
from pgzero.loaders import images, sounds
from pgzero.rect import Rect

################
## ПЕРЕМЕННЫЕ ##
################

WIDTH = 800 # размер окна
HEIGHT = 800

# Переменные игрока
PLAYER_NAME = "Виктор" # измените это на своё имя!
FRIEND1_NAME = "Саша" # измените это на имя первого друга!
FRIEND2_NAME = "Leo" # измените это на имя второго друга!
current_room = 31 # начальная комната = 31

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
PURPLE = (138, 43, 226)

air, energy = 100, 100
suit_stitched, air_fixed = False, False
launch_frame = 0


###########
## КАРТА ##
###########

MAP_WIDTH = 5
MAP_HEIGHT = 10
MAP_SIZE = MAP_WIDTH * MAP_HEIGHT

GAME_MAP = [ ["Комната 0 - где хранятся неиспользуемые объекты", 0, 0, False, False] ]

outdoor_rooms = range(1, 26)
for planetsectors in range(1, 26): # здесь создаются комнаты с 1 по 25
    GAME_MAP.append( ["Пыльная пустая поверхность Марса...", 13, 13, True, True] )

GAME_MAP += [
    # ["Название комнаты", высота, ширина, выход сверху?, выход справа?]
    ["Воздушный шлюз.", 13, 5, True, False], # комната 26
    ["Инженерная лаборатория.", 13, 13, False, False], # комната 27
    ["Центр управления полётами.", 9, 13, False, True], # комната 28
    ["Смотровая галерея.", 9, 15, False, False], # комната 29
    ["Ванная комната экипажа.", 5, 5, False, False], # комната 30
    ["Входной шлюз.", 7, 11, True, True], # комната 31
    ["Комната левого крыла.", 9, 7, True, False], # комната 32
    ["Комната правого крыла.", 7, 13, True, True], # комната 33
    ["Научная лаборатория.", 13, 13, False, True], # комната 34
    ["Оранжерея.", 13, 13, True, False], # комната 35
    [PLAYER_NAME + " спальня.", 9, 11, False, False], # комната 36
    ["Западный коридор.", 15, 5, True, True], # комната 37
    ["Комната для совещаний.", 7, 13, False, True], # комната 38
    ["Комната отдыха экипажа.", 11, 13, True, False], # комната 39
    ["Главный центр управления полётами.", 14, 14, False, False], # комната 40
    ["Боковой отсек.", 12, 7, True, False], # комната 41
    ["Западный коридор.", 9, 7, True, False], # комната 42
    ["Комната управления системами.", 9, 9, False, True], # комната 43
    ["Системный инженерный отсек.", 9, 11, False, False], # комната 44
    ["Портал безопасности в центр управления полётами.", 7, 7, True, False], # комната 45
    [FRIEND1_NAME + " спальня.", 9, 11, True, True], # комната 46
    [FRIEND2_NAME + " спальня.", 9, 11, True, True], # комната 47
    ["Трубопровод.", 13, 11, True, False], # комната 48
    ["Кабинет главного учёного.", 9, 7, True, True], # комната 49
    ["Мастерская роботов.", 9, 11, True, False] # комната 50
    ]

# простая проверка работоспособности карты выше для проверки ввода данных
assert len(GAME_MAP ) -1 == MAP_SIZE, "Размер карты и GAME_MAP не совпадают!"


#############
## ОБЪЕКТЫ ##
#############

objects = {
    0: [images.floor, None, "Пол блестящий и чистый."],
    1: [images.pillar, images.full_shadow, "Стена гладкая и холодная."],
    2: [images.soil, None, "Это похоже на пустыню. Или это должен быть десерт?"],
    3: [images.pillar_low, images.half_shadow, "Стена гладкая и холодная."],
    4: [images.bed, images.half_shadow, "Аккуратная и удобная кровать."],
    5: [images.table, images.half_shadow, "Стол. Он сделан из прочного пластика."],
    6: [images.chair_left, None, "Стул с мягкой подушкой."],
    7: [images.chair_right, None, "Стул с мягкой подушкой."],
    8: [images.bookcase_tall, images.full_shadow,
    "Книжные полки, заставленные справочниками."],
    9: [images.bookcase_small, images.half_shadow,
        "Книжные полки, заставленные справочниками."],
    10: [images.cabinet, images.half_shadow,
         "Небольшой шкафчик для хранения личных вещей."],
    11: [images.desk_computer, images.half_shadow,
         "Компьютер. Используйте его для запуска диагностики жизнеобеспечения."],
         12: [images.plant, images.plant_shadow, "Растение космической рябины, выращенное здесь."],
    13: [images.electrical1, images.half_shadow,
         "Электрические системы, используемые для питания космической станции."],
    14: [images.electrical2, images.half_shadow,
         "Электрические системы, используемые для питания космической станции."],
    15: [images.cactus, images.cactus_shadow, "Ой! Осторожнее с кактусом!"],
    16: [images.shrub, images.shrub_shadow,
    "Космический салат-латук. Немного вялый, но удивительно, что он здесь растет!"],
    17: [images.pipes1, images.pipes1_shadow, "Трубы для очистки воды."],
    18: [images.pipes2, images.pipes2_shadow,
         "Трубы для систем жизнеобеспечения."],
    19: [images.pipes3, images.pipes3_shadow,
         "Трубы для систем жизнеобеспечения."],
    20: [images.door, images.door_shadow, "Безопасная дверь. Открывается автоматически \n"
                                          "(для космонавтов в исправных скафандрах)."],
    21: [images.door, images.door_shadow, "Дверь шлюза."
         "В целях безопасности для её открытия требуется два человека."],

    # 22: [images.door, images.door_shadow, "Запертая дверь. Для её открытия требуется " \
    #  + PLAYER_NAME + " карта доступа."],

    22: [images.door, images.door_shadow, "Запертая дверь. Для её открытия требуется твоя карта доступа, "
                                          "" + PLAYER_NAME + "."],
    23: [images.door, images.door_shadow, "Запертая дверь. Нужна " \
         "карта доступа твоего первого друга (FRIEND1_NAME)."],
    24: [images.door, images.door_shadow, "Запертая дверь. Нужна " \
         "карта доступа твоего второго друга (FRIEND2_NAME)."],
    25: [images.door, images.door_shadow,
    "Запертая дверь. Она открывается из главного центра управления."],
    26: [images.door, images.door_shadow,
    "Запертая дверь в инженерном отсеке."],
    27: [images.map, images.full_shadow,
    "На экране написано, что место крушения находится в секторе:" \
        + str(LANDER_SECTOR) + " // X: " + str(LANDER_X) + \
        " // Y: " + str(LANDER_Y)],
    28: [images.rock_large, images.rock_large_shadow,
        "Камень. Его грубая поверхность похожа на точильный камень.", "Камень."],
         29: [images.rock_small, images.rock_small_shadow,
        "Маленький, но тяжёлый кусок марсианского камня."],
    30: [images.crater, None, "Кратер на поверхности планеты."],
    31: [images.fence, None,
        "Тонкая сетчатая ограда. Она помогает защитить станцию от пылевых бурь."],
    32: [images.contraption, images.contraption_shadow,
        "Один из научных экспериментов. Он мягко вибрирует."],
    33: [images.robot_arm, images.robot_arm_shadow,
        "Рука робота, используемая для подъема тяжестей."],
    34: [images.toilet, images.half_shadow, "Сверкающий чистотой туалет."],
    35: [images.sink, None, "Раковина с проточной водой.", "Краны."],
    36: [images.globe, images.globe_shadow,
        "Гигантский глобус планеты. Он мягко светится изнутри."],
    37: [images.science_lab_table, None,
        "Таблица экспериментов, анализ почвы и пыли планеты."],
    38: [images.vending_machine, images.full_shadow,
        "Торговый автомат. Для него нужен жетон.", "Торговый автомат."],
    39: [images.floor_pad, None,
        "Датчик давления, чтобы никто не выходил один."],
    40: [images.rescue_ship, images.rescue_ship_shadow, "Спасательный корабль!"],
    41: [images.mission_control_desk, images.mission_control_desk_shadow, \
        "Станции управления полётами."],
    42: [images.button, images.button_shadow,
        "Кнопка для открытия двери с временной блокировкой в инженерном деле."],
    43: [images.whiteboard, images.full_shadow,
        "Белая доска. Используется при мозговых штурмах и\nсовещаниях по планированию."],
    44: [images.window, images.full_shadow,
        "Из окна открывается вид на поверхность планеты."],
    45: [images.robot, images.robot_shadow, "Отключённый робот-уборщик."],
    46: [images.robot2, images.robot2_shadow,
        "Робот для исследования поверхности планеты, ожидающий настройки."],
    47: [images.rocket, images.rocket_shadow, "Одноместный корабль на ремонте."],
    48: [images.toxic_floor, None, "Токсичный пол — не ходите по нему!"],
    49: [images.drone, None, "Дрон-курьер"],
    50: [images.energy_ball, None, "Энергетический шар — опасно!"],
    51: [images.energy_ball2, None, "Энергетический шар — опасно!"],
    52: [images.computer, images.computer_shadow,
        "Компьютерная рабочая станция для управления системами космической станции."],
    53: [images.clipboard, None,
        "Планшет для записей. Кто-то что-то нацарапал на его листках.", "Планшет для записей."],
    54: [images.bubble_gum, None,
        "Кусочек липкой жевательной резинки. Со вкусом космической рябины.", "Жевательная резинка."],
    55: [images.yoyo, None, "Игрушка из тонкой прочной верёвки и пластика."
        "\nИспользуется для экспериментов с нулевой гравитацией.", PLAYER_NAME + "Йойо."],
    56: [images.thread, None,
        "Кусок тонкой, прочной бечевки.", "Кусок бечевки."],
    57: [images.needle, None,
        "Острая игла с растения кактуса.", "Кактусовая игла."],
    58: [images.threaded_needle, None,
        "Игла кактуса с куском бечевки.", "Игла и бечевка."],
    59: [images.canister, None,
        "Баллон с воздухом. В баллоне течь." 
        "\n\n", "Негерметичный баллон с воздухом."],
    60: [images.canister, None,
        "Похоже, пломба выдержит!", "Герметичный баллон с воздухом."],
    61: [images.mirror, None,
        "Зеркало отбрасывает круг света на стены.", "Зеркало."],
    62: [images.bin_empty, None,
        "Редкое использование мусорного ведра из лёгкого пластика.", "Мусорное ведро."],
    63: [images.bin_full, None,
        "Тяжёлое мусорное ведро, полное воды", "Мусорное ведро, полное воды."],
    64: [images.rags, None, "Промасленная тряпка. Возьми его за один угол, если нужно!", "Промасленная тряпка."],
    65: [images.hammer, None, "Молоток. Может пригодиться для того, чтобы что-то расколоть...", "Молоток."],
    66: [images.spoon, None, "Большая столовая ложка.", "Ложка."],
    67: [images.food_pouch, None,
        "Пакетик с обезвоженной едой. Ей нужна вода.", "Сухая еда."],
    68: [images.food, None,
        "Пакетик с готовой едой. Используйте его, чтобы получить 100% энергии.", "Готовая к употреблению еда."],
    69: [images.book, None, "На обложке книги большими дружелюбными буквами \
        написано: 'Не паникуй!'", "Книга."],
    70: [images.mp3_player, None,
        "MP3-плеер со всеми последними мелодиями.", "MP3-плеер."],
    71: [images.lander, None, "'Пудель' - небольшой космический аппарат. \
        В его чёрном ящике находится радиоприёмник.", "Посадочный модуль 'Пудель'"],
    72: [images.radio, None, "Система радиосвязи, взятая \
        с 'Пуделя'", "Радиостанция"],
    73: [images.gps_module, None, "Модуль GPS.", "Модуль GPS."],
    74: [images.positioning_system, None, "Часть системы позиционирования. \
        Нужен модуль GPS.", "Интерфейс позиционирования."],
    75: [images.positioning_system, None,
        "Рабочая система позиционирования.", "Компьютер для позиционирования."],
    76: [images.scissors, None, "Ножницы. Они слишком тупые, \
        чтобы что-то резать. Ты сможешь их наточить?", "Тупые ножницы."],
    77: [images.scissors, None,
        "Острые как бритва ножницы. Осторожно!", "Наточенные ножницы."],
    78: [images.credit, None,
        "Мелкая монета для станционных торговых автоматов.", "Жетон для торгового автомата."],
    79: [images.access_card, None,
        "Эта карта доступа принадлежит тебе, " + PLAYER_NAME, "Карта доступа."],
    80: [images.access_card, None,
        "Эта карта доступа принадлежит твоему первому другу (" + FRIEND1_NAME + ")", "Карта доступа."],
    81: [images.access_card, None,
        "Эта карта доступа принадлежит твоему второму другу (" + FRIEND2_NAME + ")", "Карта доступа."]
    }

items_player_may_carry = list(range(53, 82))
# Цифры ниже относятся к полу, нажимной панели, почве, токсичному полу.
items_player_may_stand_on = items_player_may_carry + [0, 39, 2, 48]


###############
## ДЕКОРАЦИИ ##
###############

# Декорации описывают объекты, которые не могут перемещаться между комнатами.
# номер комнаты: [[номер объекта, позиция по оси Y, позиция по оси X]...]
scenery = {
    26: [[39,8,2]],
    27: [[33,5,5], [33,1,1], [33,1,8], [47,5,2],
         [47,3,10], [47,9,8], [42,1,6]],
    28: [[27,0,3], [41,4,3], [41,4,7]],
    29: [[7,2,6], [6,2,8], [12,1,13], [44,0,1],
         [36,4,10], [10,1,1], [19,4,2], [17,4,4]],
    30: [[34,1,1], [35,1,3]],
    31: [[11,1,1], [19,1,8], [46,1,3]],
    32: [[48,2,2], [48,2,3], [48,2,4], [48,3,2], [48,3,3],
         [48,3,4], [48,4,2], [48,4,3], [48,4,4]],
    33: [[13,1,1], [13,1,3], [13,1,8], [13,1,10], [48,2,1],
         [48,2,7], [48,3,6], [48,3,3]],
    34: [[37,2,2], [32,6,7], [37,10,4], [28,5,3]],
    35: [[16,2,9], [16,2,2], [16,3,3], [16,3,8], [16,8,9], [16,8,2], [16,1,8],
         [16,1,3], [12,8,6], [12,9,4], [12,9,8],
         [15,4,6], [12,7,1], [12,7,11]],
    36: [[4,3,1], [9,1,7], [8,1,8], [8,1,9],
         [5,5,4], [6,5,7], [10,1,1], [12,1,2]],
    37: [[48,3,1], [48,3,2], [48,7,1], [48,5,2], [48,5,3],
         [48,7,2], [48,9,2], [48,9,3], [48,11,1], [48,11,2]],
    38: [[43,0,2], [6,2,2], [6,3,5], [6,4,7], [6,2,9], [45,1,10]],
    39: [[38,1,1], [7,3,4], [7,6,4], [5,3,6], [5,6,6],
         [6,3,9], [6,6,9], [45,1,11], [12,1,8], [12,1,4]],
    40: [[41,5,3], [41,5,7], [41,9,3], [41,9,7],
         [13,1,1], [13,1,3], [42,1,12]],
    41: [[4,3,1], [10,3,5], [4,5,1], [10,5,5], [4,7,1],
         [10,7,5], [12,1,1], [12,1,5]],
    44: [[46,4,3], [46,4,5], [18,1,1], [19,1,3],
         [19,1,5], [52,4,7], [14,1,8]],
    45: [[48,2,1], [48,2,2], [48,3,3], [48,3,4], [48,1,4], [48,1,1]],
    46: [[10,1,1], [4,1,2], [8,1,7], [9,1,8], [8,1,9], [5,4,3], [7,3,2]],
    47: [[9,1,1], [9,1,2], [10,1,3], [12,1,7], [5,4,4], [6,4,7], [4,1,8]],
    48: [[17,4,1], [17,4,2], [17,4,3], [17,4,4], [17,4,5], [17,4,6], [17,4,7],
         [17,8,1], [17,8,2], [17,8,3], [17,8,4],
         [17,8,5], [17,8,6], [17,8,7], [14,1,1]],
    49: [[14,2,2], [14,2,4], [7,5,1], [5,5,3], [48,3,3], [48,3,4]],
    50: [[45,4,8], [11,1,1], [13,1,8], [33,2,1], [46,4,6]]
    }

checksum = 0
check_counter = 0
for key, room_scenery_list in scenery.items():
    for scenery_item_list in room_scenery_list:
        checksum += (scenery_item_list[0] * key
                     + scenery_item_list[1] * (key + 1)
                     + scenery_item_list[2] * (key + 2))
        check_counter += 1
print(check_counter, "сценарные элементы")
assert check_counter == 161, "Ожидается 161 сценарный элемент"
assert checksum == 200095, "Ошибка в данных сценария"
print("Чексумма сценариев: " + str(checksum))

for room in range(1, 26):# Добавить случайные декорации для локаций на планетах.
    if room != 13: # Пропустить комнату №13.
        scenery_item = random.choice([16, 28, 29, 30])
        scenery[room] = [[scenery_item, random.randint(2, 10),
                          random.randint(2, 10)]]

# Использовать циклы для добавления ограждений для комнат на поверхности планет.
for room_coordinate in range(0, 13):
    for room_number in [1, 2, 3, 4, 5]: # Добавить ограждение сверху
        scenery[room_number] += [[31, 0, room_coordinate]]
    for room_number in [1, 6, 11, 16, 21]: # Добавить ограждение слева
        scenery[room_number] += [[31, room_coordinate, 0]]
    for room_number in [5, 10, 15, 20, 25]: # Добавить ограждение справа
        scenery[room_number] += [[31, room_coordinate, 12]]

del scenery[21][-1] # Удалить последнюю панель ограждения в комнате 21
del scenery[25][-1] # Удалить последнюю панель ограждения в комнате 25


###################
## СОЗДАТЬ КАРТУ ##
###################

def get_floor_type():
    if current_room in outdoor_rooms:
        return 2 # земля
    else:
        return 0 # плиточный пол

def generate_map():
# Эта функция создаёт карту для текущей комнаты,
# используя данные о комнате, данные о декорациях и данные о реквизите.
    global room_map, room_width, room_height, room_name, hazard_map
    global top_left_x, top_left_y, wall_transparency_frame
    room_data = GAME_MAP[current_room]
    room_name = room_data[0]
    room_height = room_data[1]
    room_width = room_data[2]

    floor_type = get_floor_type()
    if current_room in range(1, 21):
        bottom_edge = 2 #земля
        side_edge = 2 #земля
    if current_room in range(21, 26):
        bottom_edge = 1 #стена
        side_edge = 2 #земля
    if current_room > 25:
        bottom_edge = 1 #стена
        side_edge = 1 #стена

    # Создаём верхнюю линию карты комнаты.
    room_map =[[side_edge] * room_width]
    # Добавляем средние линии карты комнаты (стена, пол, заполняющий ширину, стена).
    for y in range(room_height - 2):
        room_map.append([side_edge]
                        + [floor_type]*(room_width - 2) + [side_edge])

# Добавить нижнюю линию карты комнаты.
    room_map.append([bottom_edge] * room_width)

    # Добавить дверные проёмы.
    middle_row = int(room_height / 2)
    middle_column = int(room_width / 2)

    if room_data[4]: # Если выход находится справа от этой комнаты
        room_map[middle_row][room_width - 1] = floor_type
        room_map[middle_row+1][room_width - 1] = floor_type
        room_map[middle_row-1][room_width - 1] = floor_type

    if current_room % MAP_WIDTH != 1: # If room is not on left of map
        room_to_left = GAME_MAP[current_room - 1]

    # Если в комнате слева есть выход направо, добавьте выход налево в эту комнату


        if room_to_left[4]:
            room_map[middle_row][0] = floor_type
            room_map[middle_row + 1][0] = floor_type
            room_map[middle_row - 1][0] = floor_type

    if room_data[3]: # Если выход находится в верхней части этой комнаты
        room_map[0][middle_column] = floor_type
        room_map[0][middle_column + 1] = floor_type
        room_map[0][middle_column - 1] = floor_type

    if current_room <= MAP_SIZE - MAP_WIDTH: # Если комната не находится в нижнем ряду
        room_below = GAME_MAP[current_room+MAP_WIDTH]


    # Если в комнате под вами есть верхний выход, добавьте выход в нижней части этой комнаты


        if room_below[3]:
            room_map[room_height-1][middle_column] = floor_type
            room_map[room_height-1][middle_column + 1] = floor_type
            room_map[room_height-1][middle_column - 1] = floor_type

    if current_room in scenery:
        for this_scenery in scenery[current_room]:
            scenery_number = this_scenery[0]
            scenery_y = this_scenery[1]
            scenery_x = this_scenery[2]
            room_map[scenery_y][scenery_x] = scenery_number

            image_here = objects[scenery_number][0]
            image_width = image_here.get_width()
            image_width_in_tiles = int(image_width / TILE_SIZE)

            for tile_number in range(1, image_width_in_tiles):
                room_map[scenery_y][scenery_x + tile_number] = 255

    center_y = int(HEIGHT / 2) # Центр игрового окна
    center_x = int(WIDTH / 2)
    room_pixel_width = room_width * TILE_SIZE # Размер комнаты в пикселях
    room_pixel_height = room_height * TILE_SIZE
    top_left_x = center_x - 0.5 * room_pixel_width
    top_left_y = (center_y - 0.5 * room_pixel_height) + 110

    for prop_number, prop_info in props.items():
        prop_room = prop_info[0]
        prop_y = prop_info[1]
        prop_x = prop_info[2]
        if (prop_room == current_room and
            room_map[prop_y][prop_x] in [0, 39, 2]):
                room_map[prop_y][prop_x] = prop_number
                image_here = objects[prop_number][0]
                image_width = image_here.get_width()
                image_width_in_tiles = int(image_width / TILE_SIZE)
                for tile_number in range(1, image_width_in_tiles):
                    room_map[prop_y][prop_x + tile_number] = 255

    hazard_map = [] # пустой список
    for y in range(room_height):
        hazard_map.append( [0] * room_width )


###############
## ЦИКЛ ИГРЫ ##
###############

def start_room():
    global airlock_door_frame
    show_text("Ты находишься в комнате: " + room_name, 0)
    if current_room == 26: # Комната с самозакрывающейся дверью шлюза
        airlock_door_frame = 0
    clock.schedule_interval(door_in_room_26, 0.05)
    hazard_start()

def game_loop():
    global player_x, player_y, current_room
    global from_player_x, from_player_y
    global player_image, player_image_shadow
    global selected_item, item_carrying, energy
    global player_offset_x, player_offset_y
    global player_frame, player_direction

    if game_over:
        return

    if player_frame > 0:
        player_frame += 1
        time.sleep(0.05)
        if player_frame == 5:
            player_frame = 0
            player_offset_x = 0
            player_offset_y = 0

# сохраняем текущее положение игрока
    old_player_x = player_x
    old_player_y = player_y

# перемещаемся, если нажата клавиша
    if player_frame == 0:
        if keyboard.right:
            from_player_x = player_x
            from_player_y = player_y
            player_x += 1
            player_direction = "right"
            player_frame = 1
        elif keyboard.left: #elif останавливает игрока при диагональных движениях
            from_player_x = player_x
            from_player_y = player_y
            player_x -= 1
            player_direction = "left"
            player_frame = 1
        elif keyboard.up:
            from_player_x = player_x
            from_player_y = player_y
            player_y -= 1
            player_direction = "up"
            player_frame = 1
        elif keyboard.down:
            from_player_x = player_x
            from_player_y = player_y
            player_y += 1
            player_direction = "down"
            player_frame = 1

# проверка на выход из комнаты
    if player_x == room_width: # через дверь справа
        clock.unschedule(hazard_move)
        current_room += 1
        generate_map()
        player_x = 0 # войти слева
        player_y = int(room_height / 2) # войти через дверь
        player_frame = 0
        start_room()
        return

    if player_x == -1: # через дверь слева
        clock.unschedule(hazard_move)
        current_room -= 1
        generate_map()
        player_x = room_width - 1  # войти справа
        player_y = int(room_height / 2) # войти через дверь
        player_frame = 0
        start_room()
        return

    if player_y == room_height: # через дверь внизу
        clock.unschedule(hazard_move)
        current_room += MAP_WIDTH
        generate_map()
        player_y = 0 # войти сверху
        player_x = int(room_width / 2) # войти через дверь
        player_frame = 0
        start_room()
        return

    if player_y == -1: # через дверь сверху
        clock.unschedule(hazard_move)
        current_room -= MAP_WIDTH
        generate_map()
        player_y = room_height - 1 # войти снизу
        player_x = int(room_width / 2) # войти через дверь
        player_frame = 0
        start_room()
        return

    if keyboard.g:
        pick_up_object()

    if keyboard.tab and len(in_my_pockets) > 0:
        selected_item += 1
        if selected_item > len(in_my_pockets) - 1:
            selected_item = 0
        item_carrying = in_my_pockets[selected_item]
        display_inventory()
        time.sleep(0.2)

    if keyboard.d and item_carrying:
        drop_object(old_player_y, old_player_x)

    if keyboard.space:
        examine_object()

    if keyboard.u:
        use_object()

#### Телепорт для тестирования
#### Удалите этот раздел для реальной игры
##    if keyboard.x:
##        current_room = int(input("Введите номер комнаты:"))
##        player_x = 2
##        player_y = 2
##        generate_map()
##        start_room()
##        sounds.teleport.play()
#### Раздел телепортации завершен

  # Если игрок стоит там, где ему не следует находиться, переместите его обратно.
    if room_map[player_y][player_x] not in items_player_may_stand_on \
               or hazard_map[player_y][player_x] != 0:
        player_x = old_player_x
        player_y = old_player_y
        player_frame = 0

    if room_map[player_y][player_x] == 48: # токсичный пол
        deplete_energy(1)

    if player_direction == "right" and player_frame > 0:
        player_offset_x = -1 + (0.25 * player_frame)
    if player_direction == "left" and player_frame > 0:
        player_offset_x = 1 - (0.25 * player_frame)
    if player_direction == "up" and player_frame > 0:
        player_offset_y = 1 - (0.25 * player_frame)
    if player_direction == "down" and player_frame > 0:
        player_offset_y = -1 + (0.25 * player_frame)


#############
##  ПОКАЗ  ##
#############

def draw_image(image, y, x):
    screen.blit(
        image,
        (top_left_x + (x * TILE_SIZE),
         top_left_y + (y * TILE_SIZE) - image.get_height())
        )

def draw_shadow(image, y, x):
    screen.blit(
        image,
        (top_left_x + (x * TILE_SIZE),
         top_left_y + (y * TILE_SIZE))
        )

def draw_player():
    player_image = PLAYER[player_direction][player_frame]
    draw_image(player_image, player_y + player_offset_y,
               player_x + player_offset_x)
    image_player_shadow = PLAYER_SHADOW[player_direction][player_frame]
    draw_shadow(image_player_shadow, player_y + player_offset_y,
                player_x + player_offset_x)

def draw():
    if game_over:
        return

    # Очистите игровую арену.
    box = Rect((0, 178), (800, 570))
    screen.draw.filled_rect(box, RED)
    box = Rect ((0, 0), (800, top_left_y + (room_height - 1)*30))
    screen.surface.set_clip(box)
    floor_type = get_floor_type()

    for y in range(room_height): # Выкладываем плитки пола, затем предметы на полу.
        for x in range(room_width):
            draw_image(objects[floor_type][0], y, x)
            # Следующая строка позволяет теням падать на предметы на полу
            if room_map[y][x] in items_player_may_stand_on:
                draw_image(objects[room_map[y][x]][0], y, x)

    # Накладка в комнате 26 добавлена здесь, чтобы на неё можно было ставить предметы.
    if current_room == 26:
        draw_image(objects[39][0], 8, 2)
        image_on_pad = room_map[8][2]
        if image_on_pad > 0:
            draw_image(objects[image_on_pad][0], 8, 2)

    for y in range(room_height):
        for x in range(room_width):
            item_here = room_map[y][x]
    # Игрок не может ходить по 255: это обозначает места, используемые широкими объектами.
            if item_here not in items_player_may_stand_on + [255]:
                image = objects[item_here][0]

                if (current_room in outdoor_rooms
                    and y == room_height - 1
                    and room_map[y][x] == 1) or \
                    (current_room not in outdoor_rooms
                    and y == room_height - 1
                    and room_map[y][x] == 1
                    and x > 0
                    and x < room_width - 1):

    # Добавить прозрачное изображение стены в первом ряду.
                    image = PILLARS[wall_transparency_frame]
                draw_image(image, y, x)

                if objects[item_here][1] is not None: # Если у объекта есть тень

                    shadow_image = objects[item_here][1]

    # если тени может потребоваться горизонтальная разметка
                    if shadow_image in [images.half_shadow,
                                        images.full_shadow]:
                        shadow_width = int(image.get_width() / TILE_SIZE)

    # Использовать тень по ширине объекта.
                        for z in range(0, shadow_width):
                            draw_shadow(shadow_image, y, x+z)
                    else:
                        draw_shadow(shadow_image, y, x)

            hazard_here = hazard_map[y][x]
            if hazard_here != 0: # Если в этой позиции есть опасность
                draw_image(objects[hazard_here][0], y, x)

        if (player_y == y):
                draw_player()

    screen.surface.set_clip(None)

def adjust_wall_transparency():
    global wall_transparency_frame

    if (player_y == room_height - 2
        and room_map[room_height - 1][player_x] == 1
        and wall_transparency_frame < 4):
        wall_transparency_frame += 1 # Стена становится прозрачной (out).

    if ((player_y < room_height - 2
            or room_map[room_height - 1][player_x] != 1)
            and wall_transparency_frame > 0):
        wall_transparency_frame -= 1 # Стена становится прозрачной (in).

def show_text(text_to_show, line_number):
    if game_over:
        return
    if line_number == 0: # цвет текста в зависимости от номера линии вывода
        color = PURPLE
    elif line_number == 1:
        color = RED
    else: color = WHITE
    text_lines = [15, 55] # координата Y в зависимости от номера линии вывода
    box = Rect((0, text_lines[line_number]), (800, 35))
    screen.draw.filled_rect(box, BLACK)
    screen.draw.text(text_to_show,
                     (20, text_lines[line_number]), color=color)


##############
## ПРЕДМЕТЫ ##
##############

# Предметы — это объекты, которые могут перемещаться между комнатами, появляться или исчезать.
# Весь реквизит должен быть установлен здесь. Предмет, которого ещё нет в игре, отправляется в комнату 0.
# номер объекта: [комната, y, x]

props = {
    20: [31, 0, 4], 21: [26, 0, 1], 22: [41, 0, 2], 23: [39, 0, 5],
    24: [45, 0, 2],
    25: [32, 0, 2], 26: [27, 12, 5],  # две стороны одной двери
    40: [0, 8, 6], 53: [45, 1, 5], 54: [0, 0, 0], 55: [0, 0, 0],
    56: [0, 0, 0], 57: [35, 4, 6], 58: [0, 0, 0], 59: [31, 1, 7],
    60: [0, 0, 0], 61: [36, 1, 1], 62: [36, 1, 6], 63: [0, 0, 0],
    64: [27, 8, 3], 65: [50, 1, 7], 66: [39, 5, 6], 67: [46, 1, 1],
    68: [0, 0, 0], 69: [30, 3, 3], 70: [47, 1, 3],
    71: [0, LANDER_Y, LANDER_X], 72: [0, 0, 0], 73: [27, 4, 6],
    74: [28, 1, 11], 75: [0, 0, 0], 76: [41, 3, 5], 77: [0, 0, 0],
    78: [35, 9, 11], 79: [26, 3, 2], 80: [41, 7, 5], 81: [29, 1, 1]
    }

checksum = 0

for key, prop in props.items():
    if key != 71:  # 71 пропускается, потому что в каждой игре он разный.
        checksum += (prop[0] * key
                     + prop[1] * (key + 1)
                     + prop[2] * (key + 2))
print(len(props), "предметы")
assert len(props) == 37, "Ожидалось 37 элементов реквизита"
print("Контрольная сумма реквизита:", checksum)
assert checksum == 61414, "Ошибка в данных предмета"


in_my_pockets = [55]
selected_item = 0  # первый элемент
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
assert len(RECIPES) == 11, "Ожидалось 11 рецептов"
assert checksum == 37296, "Ошибка в данных рецептов"
print("Чек-сумма рецептов:", checksum)



#################################
## ВЗАИМОДЕЙСТВИЕ С ПРЕДМЕТАМИ ##
#################################

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
    # Получить номер объекта в местоположении игрока.

    item_player_is_on = get_item_under_player()
    if item_player_is_on in items_player_may_carry:

    # Очистить место на полу.

        room_map[player_y][player_x] = get_floor_type()
        add_object(item_player_is_on)
        show_text("Теперь в твоём рюкзаке: " + objects[item_player_is_on][3], 0)
        sounds.pickup.play()
        time.sleep(0.5)
    else:
        show_text("Ты не можешь взять это!", 0)

def add_object(item):  # Добавляет предмет в инвентарь.
    global selected_item, item_carrying
    in_my_pockets.append(item)
    item_carrying = item
    # Минус один, потому что индексы начинаются с 0.
    selected_item = len(in_my_pockets) - 1
    display_inventory()
    props[item][0] = 0  # Переносимые предметы попадают в комнату 0 (вне карты).

def display_inventory():
    box = Rect((0, 100), (800, 95))
    screen.draw.filled_rect(box, BLACK)

    if len(in_my_pockets) == 0:
        return

    start_display = (selected_item // 16) * 16
    list_to_show = in_my_pockets[start_display : start_display + 16]
    selected_marker = selected_item % 16

    for item_counter in range(len(list_to_show)):
        item_number = list_to_show[item_counter]
        image = objects[item_number][0]
        screen.blit(image, (25 + (46 * item_counter), 100))

    box_left = (selected_marker * 46) - 3
    box = Rect((22 + box_left, 95), (40, 40))
    screen.draw.rect(box, WHITE)
    item_highlighted = in_my_pockets[selected_item]
    description = objects[item_highlighted][2]
    screen.draw.text(description, (20, 140), color="white")

def drop_object(old_y, old_x):
    global room_map, props
    if room_map[old_y][old_x] in [0, 2, 39]: # место, где вы можете бросить вещь
        props[item_carrying][0] = current_room
        props[item_carrying][1] = old_y
        props[item_carrying][2] = old_x
        room_map[old_y][old_x] = item_carrying
        show_text("Ты бросил" + objects[item_carrying][3], 0)
        sounds.drop.play()
        remove_object(item_carrying)
        time.sleep(0.5)
    else: # Это происходит только в том случае, если здесь уже есть предмет
        show_text("Ты не можишь бросить это здесь!", 0)
        time.sleep(0.5)

def remove_object(item): # Удаляет предмет из инвентаря
    global selected_item, in_my_pockets, item_carrying
    in_my_pockets.remove(item)
    selected_item = selected_item - 1
    if selected_item < 0:
        selected_item = 0
    if len(in_my_pockets) == 0:  # Если в них ничего нет
        item_carrying = False  # Установите item_carrying в значение False
    else:  # В противном случае установите его в значение нового выбранного предмета
        item_carrying = in_my_pockets[selected_item]
    display_inventory()

def examine_object():
    item_player_is_on = get_item_under_player()
    left_tile_of_item = find_object_start_x()
    if item_player_is_on in [0, 2]:  # не описывайте пол
        return
    description = "Ты видишь: " + objects[item_player_is_on][2]
    for prop_number, details in props.items():
        # предметы = номер объекта: [номер комнаты, y, x]
        if details[0] == current_room:  # если предмет находится в комнате
            # Если предмет скрыт (= находится в месте игрока, но не на карте)

            if (details[1] == player_y
                and details[2] == left_tile_of_item
                and room_map[details[1]][details[2]] != prop_number):
                add_object(prop_number)
                description = "Ты нашёл: " + objects[prop_number][3]
                sounds.combine.play()
    show_text(description, 0)
    time.sleep(0.5)


############################
## ИСПОЛЬЗОВАНИЕ ОБЪЕКТОВ ##
############################

def use_object():
    global room_map, props, item_carrying, air, selected_item, energy
    global in_my_pockets, suit_stitched, air_fixed, game_over

    use_message = "Ты пытаешься это использовать, но ничего не получается."

    standard_responses = {

        4: "Воздух заканчивается! Ты не можешь просто так это оставить!",
        6: "Сейчас не время сидеть сложа руки!",
        7: "Сейчас не время сидеть сложа руки!",
        32: "Всё трясётся и грохочет, но больше ничего не происходит.",
        34: "Ах! Так-то лучше. Теперь вымой руки.",
        35: "Ты моешь руки и стряхиваешь воду.",
        37: "Пробирки слегка дымятся, когда ты их встряхиваешь.",
        54: "Ты жуёшь жвачку. Она липкая, как клей.",
        55: "Йойо подпрыгивает вверх и вниз - чуть медленнее, чем на Земле.",
        56: "Это немного сложно. Ты можешь привязать его к чему-нибудь?",
        59: "Нужно устранить утечку, прежде чем ты сможешь использовать баллон!",
        61: "Ты пытаешься подать сигнал с помощью зеркала, но тебя никто не видит.",
        62: "Не трать ресурсы впустую. Вещи могут пригодиться...",
        67: "Чтобы насладиться вкусной космической едой, просто добавь воды!",
        75: "Ты находишься в секторе: " + str(current_room) + " // X: " \
        + str(player_x) + " // Y: " + str(player_y)
    }

    # Получить номер объекта в местоположении игрока.
    item_player_is_on = get_item_under_player()
    for this_item in [item_player_is_on, item_carrying]:
        if this_item in standard_responses:
            use_message = standard_responses[this_item]

    if item_carrying == 70 or item_player_is_on == 70:
        use_message = "Оглушающие звуки!"
        sounds.steelmusic.play(2)

    elif item_player_is_on == 11:
        use_message = "AIR: " + str(air) + \
                      "% / ENERGY " + str(energy) + "% / "
        if not suit_stitched:
            use_message += "*ALERT* SUIT FABRIC TORN / "
        if not air_fixed:
            use_message += "*ALERT* SUIT AIR BOTTLE MISSING"
        if suit_stitched and air_fixed:
            use_message += " SUIT OK"
        show_text(use_message, 0)
        sounds.say_status_report.play()
        time.sleep(0.5)

    # Если "на" компьютере, игрок явно хочет обновить статус.
    # Вернитесь, чтобы остановить использование другого объекта, случайно заменившего этот.


        return

    elif item_carrying == 60 or item_player_is_on == 60:
        use_message = "Ты прикрепляешь " + objects[60][3] + " к костюму"
        air_fixed = True
        air = 90
        air_countdown()
        remove_object(60)

    elif (item_carrying == 58 or item_player_is_on == 58) \
       and not suit_stitched:
        use_message = "Ты используешь" + objects[56][3] + \
                      " для починки ткани костюма"
        suit_stitched = True
        remove_object(58)

    elif item_carrying == 72 or item_player_is_on == 72:
        use_message = "Ты вызываешь помощь по радио. Приближается спасательный корабль. \
            Сектор встречи 13, снаружи"
        props[40][0] = 13

    elif (item_carrying == 66 or item_player_is_on == 66) \
            and current_room in outdoor_rooms:
        use_message = "Ты копаешь..."
        if (current_room == LANDER_SECTOR
            and player_x == LANDER_X
            and player_y == LANDER_Y):
            add_object(71)
            use_message = "Ты нашел посадочный модуль!"

    elif item_player_is_on == 40:
        clock.unschedule(air_countdown)
        show_text("Поздравляю, "+ PLAYER_NAME +"!", 0)
        show_text("Миссия выполнена! Ты добрался до безопасного места.", 1)
        game_over = True
        sounds.take_off.play()
        game_completion_sequence()

    elif item_player_is_on == 16:
        energy += 1
        if energy > 100:
            energy = 100
        use_message = "Ты жуёшь салат и получаешь немного энергии обратно"
        draw_energy_air()

    elif item_player_is_on == 42:
        if current_room == 27:
            open_door(26)
        props[25][0] = 0  # Дверь из RM32 в инженерный отсек
        props[26][0] = 0  # Дверь внутри инженерного отсека
        clock.schedule_unique(shut_engineering_door, 60)
        use_message = "Ты нажимаешь кнопку."
        show_text("Дверь в инженерный отсек открыта в течение 60 секунд.", 1)
        sounds.say_doors_open.play()
        sounds.doors.play()

    elif item_carrying == 68 or item_player_is_on == 68:
        energy = 100
        use_message = "Ты используешь еду, чтобы восстановить энергию."
        remove_object(68)
        draw_energy_air()

    if suit_stitched and air_fixed: # открыть доступ в шлюз
        if current_room == 31 and props[20][0] == 31:
            open_door(20) # включая снятие двери
            sounds.say_airlock_open.play()
            show_text("Компьютер сообщил тебе, что воздушный шлюз открыт", 1)
        elif props[20][0] == 31:
            props[20][0] = 0 # удалить дверь с карты
            sounds.say_airlock_open.play()
            show_text("Компьютер сообщил тебе, что воздушный шлюз открыт", 1)

    for recipe in RECIPES:
        ingredient1 = recipe[0]
        ingredient2 = recipe[1]
        combination = recipe[2]
        if (item_carrying == ingredient1
            and item_player_is_on == ingredient2) \
            or (item_carrying == ingredient2
                and item_player_is_on == ingredient1):
            use_message = "Ты соединяешь " + objects[ingredient1][3] \
                          + " и " + objects[ingredient2][3] \
                          + " и получаешь " + objects[combination][3]


            if item_player_is_on in props.keys():
                props[item_player_is_on][0] = 0
                room_map[player_y][player_x] = get_floor_type()
            in_my_pockets.remove(item_carrying)
            add_object(combination)
            sounds.combine.play()

    # {key object number: door object number}
    ACCESS_DICTIONARY = { 79:22, 80:23, 81:24 }
    if item_carrying in ACCESS_DICTIONARY:
        door_number = ACCESS_DICTIONARY[item_carrying]
        if props[door_number][0] == current_room:
            use_message = "Ты открываешь двери!"
            sounds.say_doors_open.play()
            sounds.doors.play()
            open_door(door_number)

    show_text(use_message, 0)
    time.sleep(0.5)

def game_completion_sequence():
    global launch_frame #(начальное значение равно 0, задано в разделе ПЕРЕМЕННЫЕ)
    box = Rect((0, 150), (800, 600))
    screen.draw.filled_rect(box, (128, 0, 0))
    box = Rect ((0, top_left_y - 30), (800, 390))
    screen.surface.set_clip(box)

    for y in range(0, 13):
        for x in range(0, 13):
            draw_image(images.soil, y, x)

    launch_frame += 1
    if launch_frame < 9:
        draw_image(images.rescue_ship, 8 - launch_frame, 6)
        draw_shadow(images.rescue_ship_shadow, 8 + launch_frame, 6)
        clock.schedule(game_completion_sequence, 0.25)
    else:
        screen.surface.set_clip(None)
        screen.draw.text("МИССИЯ", (200, 380), color = "white",
                     fontsize = 128, shadow = (1, 1), scolor = "black")
        screen.draw.text("ЗАВЕРШЕНА", (145, 480), color = "white",
                     fontsize = 128, shadow = (1, 1), scolor = "black")
        sounds.completion.play()
        sounds.say_mission_complete.play()


    ###########
    ## ДВЕРИ ##
    ###########

def open_door(opening_door_number):
    global door_frames, door_shadow_frames
    global door_frame_number, door_object_number
    door_frames = [images.door1, images.door2, images.door3,
                   images.door4, images.floor]
    # (Последний кадр восстанавливает тень, чтобы она была готова к повторному появлению двери).
    door_shadow_frames = [images.door1_shadow, images.door2_shadow,
                          images.door3_shadow, images.door4_shadow,
                          images.door_shadow]
    door_frame_number = 0
    door_object_number = opening_door_number
    do_door_animation()

def close_door(closing_door_number):
    global door_frames, door_shadow_frames
    global door_frame_number, door_object_number, player_y
    door_frames = [images.door4, images.door3, images.door2,
                   images.door1, images.door]
    door_shadow_frames = [images.door4_shadow, images.door3_shadow,
                          images.door2_shadow, images.door1_shadow,
                          images.door_shadow]
    door_frame_number = 0
    door_object_number = closing_door_number
    # Если игрок находится в том же ряду, что и дверь, он должен быть в открытом дверном проёме
    if player_y == props[door_object_number][1]:
        if player_y == 0: # если в верхнем дверном проёме
            player_y = 1 # переместить их вниз
        else:
            player_y = room_height - 2  # переместить их вверх
    do_door_animation()

def do_door_animation():
    global door_frames, door_frame_number, door_object_number, objects
    objects[door_object_number][0] = door_frames[door_frame_number]
    objects[door_object_number][1] = door_shadow_frames[door_frame_number]
    door_frame_number += 1
    if door_frame_number == 5:
        if door_frames[-1] == images.floor:
            props[door_object_number][0] = 0 # удалить дверь из списка реквизита
        # Пересчитать карту комнаты из реквизита
        # чтобы при необходимости поместить дверь в комнату.
        generate_map()
    else:
        clock.schedule(do_door_animation, 0.15)

def shut_engineering_door():
    global current_room, door_room_number, props
    props[25][0] = 32  # Дверь из комнаты 32 в инженерный отсек.
    props[26][0] = 27  # Дверь внутри инженерного отсека.
    generate_map()  # Добавить дверь на карту комнаты, если она находится в нужной комнате.
    if current_room == 27:

        close_door(26)
    if current_room == 32:
        close_door(25)
    show_text("Компьютер сообщает, что двери закрыты.", 1)
    sounds.say_doors_closed.play()

def door_in_room_26():
    global airlock_door_frame, room_map
    frames = [images.door, images.door1, images.door2,
              images.door3,images.door4, images.floor
              ]

    shadow_frames = [images.door_shadow, images.door1_shadow,
                     images.door2_shadow, images.door3_shadow,
                     images.door4_shadow, None]

    if current_room != 26:
        clock.unschedule(door_in_room_26)
        return

    # реквизит 21 — это дверь в комнате 26.
    if ((player_y == 8 and player_x == 2) or props[63] == [26, 8, 2]) \
            and props[21][0] == 26:
        airlock_door_frame += 1
        if airlock_door_frame == 5:
            props[21][0] = 0 # Убрать дверь с карты, когда она полностью открыта.
            room_map[0][1] = 0
            room_map[0][2] = 0
            room_map[0][3] = 0

    if ((player_y != 8 or player_x != 2) and props[63] != [26, 8, 2]) \
            and airlock_door_frame > 0:
        if airlock_door_frame == 5:
            # Добавьте дверь в список предметов и на карту, чтобы отображалась анимация.
            props[21][0] = 26
            room_map[0][1] = 21
            room_map[0][2] = 255
            room_map[0][3] = 255
        airlock_door_frame -= 1

    objects[21][0] = frames[airlock_door_frame]
    objects[21][1] = shadow_frames[airlock_door_frame]


###############
##    AIR    ##
###############

def draw_energy_air():
    box = Rect((10, 765), (500, 20))
    screen.draw.filled_rect(box, BLACK)
    screen.draw.text("ВОЗДУХ", (10, 768), color=BLUE)
    screen.draw.text("ЭНЕРГИЯ", (200, 768), color=YELLOW)

    if air > 0:
        box = Rect((86, 765), (air, 20))
        screen.draw.filled_rect(box, BLUE) # Нарисовать новую шкалу для воздуха.

    if energy > 0:
        box = Rect((285, 765), (energy, 20))
        screen.draw.filled_rect(box, YELLOW) # Нарисовать новую шкалу для энергии.

def end_the_game(reason):
    global game_over
    show_text(reason, 1)
    game_over = True
    sounds.say_mission_fail.play()
    sounds.gameover.play()
    screen.draw.text("ИГРА ОКОНЧЕНА", (11, 400), color = "white",
                     fontsize = 128, shadow = (1, 1), scolor = "black")

def air_countdown():
    global air, game_over
    if game_over:
        return # Не расходуйте воздух, если они уже мертвы.
    air -= 1
    if air == 20:
        sounds.say_air_low.play()
    if air == 10:
        sounds.say_act_now.play()
    draw_energy_air()
    if air < 1:
        end_the_game("У тебя закончился воздух!")

def alarm():
    show_text("Заканчивается воздух, " + PLAYER_NAME
              + "!\nДоберись до безопасного места и вызови помощь по радиосвязи!", 1)
    sounds.alarm.play(3)
    sounds.say_breach.play()


    ###############
    ## ОПАСНОСТИ ##
    ###############

hazard_data = {
    # room number: [[y, x, direction, bounce addition to direction]]
    28: [[1, 8, 2, 1], [7, 3, 4, 1]], 32: [[1, 5, 4, -1]],
    34: [[5, 1, 1, 1], [5, 5, 1, 2]], 35: [[4, 4, 1, 2], [2, 5, 2, 2]],
    36: [[2, 1, 2, 2]], 38: [[1, 4, 3, 2], [5, 8, 1, 2]],
    40: [[3, 1, 3, -1], [6, 5, 2, 2], [7, 5, 4, 2]],
    41: [[4, 5, 2, 2], [6, 3, 4, 2], [8, 1, 2, 2]],
    42: [[2, 1, 2, 2], [4, 3, 2, 2], [6, 5, 2, 2]],
    46: [[2, 1, 2, 2]],
    48: [[1, 8, 3, 2], [8, 8, 1, 2], [3, 9, 3, 2]]
    }

def deplete_energy(penalty):
    global energy, game_over
    if game_over:
        return # Не отнимайте энергию, если они уже мертвы.
    energy = energy - penalty
    draw_energy_air()
    if energy < 1:
        end_the_game("У тебя закончилась энергия!")

def hazard_start():
    global current_room_hazards_list, hazard_map
    if current_room in hazard_data.keys():
        current_room_hazards_list = hazard_data[current_room]
        for hazard in current_room_hazards_list:
            hazard_y = hazard[0]
            hazard_x = hazard[1]
            hazard_map[hazard_y][hazard_x] = 49 + (current_room % 3)
        clock.schedule_interval(hazard_move, 0.15)

def hazard_move():
    global current_room_hazards_list, hazard_data, hazard_map
    global old_player_x, old_player_y

    if game_over:
        return

    for hazard in current_room_hazards_list:
        hazard_y = hazard[0]
        hazard_x = hazard[1]
        hazard_direction = hazard[2]

        old_hazard_x = hazard_x
        old_hazard_y = hazard_y
        hazard_map[old_hazard_y][old_hazard_x] = 0

        if hazard_direction == 1: # сверху
            hazard_y -= 1
        if hazard_direction == 2: # справа
            hazard_x += 1
        if hazard_direction == 3: # снизу
            hazard_y += 1
        if hazard_direction == 4: # слева
            hazard_x -= 1

        hazard_should_bounce = False

        if (hazard_y == player_y and hazard_x == player_x) or \
           (hazard_y == from_player_y and hazard_x == from_player_x
            and player_frame > 0):
            sounds.ouch.play()
            deplete_energy(10)
            hazard_should_bounce = True

        # Не дать опасности выйти за дверь
        if hazard_x == room_width:
            hazard_should_bounce = True
            hazard_x = room_width - 1
        if hazard_x == -1:
            hazard_should_bounce = True
            hazard_x = 0
        if hazard_y == room_height:
            hazard_should_bounce = True
            hazard_y = room_height - 1
        if hazard_y == -1:
            hazard_should_bounce = True
            hazard_y = 0

        # Остановиться, когда опасность столкнётся с декорацией или другой опасностью.
        if room_map[hazard_y][hazard_x] not in items_player_may_stand_on \
               or hazard_map[hazard_y][hazard_x] != 0:
            hazard_should_bounce = True

        if hazard_should_bounce:
            hazard_y = old_hazard_y # Вернёмся к последней допустимой позиции.
            hazard_x = old_hazard_x
            hazard_direction += hazard[3]
            if hazard_direction > 4:
                hazard_direction -= 4
            if hazard_direction < 1:
                hazard_direction += 4
            hazard[2] = hazard_direction

        hazard_map[hazard_y][hazard_x] = 49 + (current_room % 3)
        hazard[0] = hazard_y
        hazard[1] = hazard_x


###############
##   СТАРТ   ##
###############

generate_map()
clock.schedule_interval(game_loop, 0.03)
clock.schedule_interval(adjust_wall_transparency, 0.05)
clock.schedule_unique(display_inventory, 1)
clock.schedule_unique(draw_energy_air, 0.5)
clock.schedule_unique(alarm, 10)
# Чем больше число, тем больше дается времени.
clock.schedule_interval(air_countdown, 5)
sounds.mission.play() # Вступительная музыка

pgzrun.go()