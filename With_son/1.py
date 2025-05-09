import pgzero
import pgzrun
import clock
from pgzero.keyboard import keyboard
from pgzero.loaders import images
from pgzero.clock import clock
from pgzero.rect import Rect

screen: pgzero.screen.Screen
keyboard: pgzero.keyboard.Keyboard
#from pgzero.screen import Screen

WIDTH = 800
HEIGHT = 550
player_x = 500
player_y = 350
slogan_x = 800
slogan_y = 50

PURPLE = (138, 43, 226)
BLACK = (0, 0, 0)
def draw():
    screen.blit(images.backdrop, (0, 0))
    screen.blit(images.mars, (300, 150))
    start(slogan_x, slogan_y)
    screen.blit(images.astronaut,(player_x, player_y))
    screen.blit(images.rocket, (150, 90))

def show_text(text_to_show, slogan_x, slogan_y):
    text_lines = [15,50]
    # box = Rect((20,text_lines[lines]), (400,35))
    # screen.draw.filled_rect(box, BLACK)
    screen.draw.text(text_to_show, (slogan_x, slogan_y), color=PURPLE, fontsize = 60)

def start(slogan_x, slogan_y):
    show_text("Здравствуй, Виктор!", slogan_x, slogan_y)


def move():
    global player_x, player_y, slogan_x, slogan_y
    # управление космонавтом
    if keyboard.left:
        player_x -= 5
        print(player_x)
    elif keyboard.right:
        player_x += 5
    elif keyboard.up:
        player_y -= 5
    elif keyboard.down:
        player_y += 5

    # управление лозунгом
    if keyboard.A:
        slogan_x -= 5
    elif keyboard.D:
        slogan_x += 5

clock.schedule_interval(move, 0.03)

pgzrun.go()