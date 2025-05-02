# -*- coding: utf-8 -*-
# Author: Metalofon

"""Программа
для движения квадрата в окне pygame с очень подробным описанием всего, что происходит.
Автор программы: Metalofon
"""

# Импорты модулей
import pygame  # Импортируем модуль pygame

# Константы
WHITE_COLOR = (255, 255, 255)  # Белый цвет
BLUE_COLOR = (0, 0, 255)  # Синий цвет
WIN_SIZE = (640, 480)  # Размер окна
WIN_CAPTION = "Rect Move"  # Заголовок окна
START_POSITION = (0, 0)  # Стартовая позиция игрока
START_TURN = (1, 1)  # Стартовое направление игрока
PLAYER_SIZE = (40, 40)  # Размеры игрока
MOVE_SPEED = (120, 120)  # Скорость игрока
X, Y = range(2)  # Enum для координат
POS, TURN = "pos", "turn"  # Константы для удобства

# Инициализация модуля pygame
pygame.init()  # Инициализируем модуль pygame

# Ссылки
display_ = pygame.display  # Работа с экраном
time_ = pygame.time  # Работа с временем
event_ = pygame.event  # Работа с событиями
draw_ = pygame.draw  # Работа с рисованием

# Окно
window = display_.set_mode(WIN_SIZE)  # Создаём окно и задаём его размеры
display_.set_caption(WIN_CAPTION)  # Задаём заголовок окна

# Таймер
timer = time_.Clock()  # Создаём таймер

# Программные переменные
run = True  # Запущена ли программа?
delta_time = 0  # DeltaTime

# Игровые переменные
player = {"pos": list(START_POSITION), "turn": list(START_TURN)}  # Переменные игрока

# Главный цикл
while run:  # Пока программа запущена

    # Задержка и DeltaTime
    delta_time = timer.tick() / 1000  # Получаем DeltaTime

    # События
    for event in event_.get():  # Проходим по всем событиям
        if event.type == pygame.QUIT:  # Если событие нажатия на крестик закрытия окна
            run = False  # Выключаем программу

    # Логика
    player[POS][X] += (MOVE_SPEED[X] *  # Скорость движения по X
                       player[TURN][X] *  # Направление игрока по X
                       delta_time  # DeltaTime
                       )  # Двигаем игрока по X координате
    player[POS][Y] += (MOVE_SPEED[Y] *  # Скорость движения по Y
                       player[TURN][Y] *  # Направление игрока по Y
                       delta_time  # DeltaTime
                       )  # Двигаем игрока по Y координате

    if (
            player[POS][X] <= 0 or  # Если игрок вышел за левую границу экрана
            player[POS][X] + PLAYER_SIZE[X] >= WIN_SIZE[X]  # Если игрок вышел за правую границу экрана
    ):  # Проверка выхода за экран по X
        player[TURN][X] *= -1  # Смена направления X
    if (
            player[POS][Y] <= 0 or  # Если игрок вышел за вершнюю границу экрана
            player[POS][Y] + PLAYER_SIZE[Y] >= WIN_SIZE[Y]  # Если игрок вышел за нижнюю границу экрана
    ):  # Проверка выхода за экран по Y
        player[TURN][Y] *= -1  # Смена направления Y

    # Рисование
    window.fill(WHITE_COLOR)  # Заливка экрана белым цветом (Очистка экрана)

    draw_.rect(window, BLUE_COLOR, (  # Рисуем прямоугольник
        player[POS],  # Координаты прямоугольника
        PLAYER_SIZE  # Размер прямоугольника
    ))

    display_.update()  # Обновление экрана

pygame.quit()  # Выходим из модуля pygame