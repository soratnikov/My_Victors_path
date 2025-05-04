import pgzero
import pgzrun
from pgzero.loaders import images

screen: pgzero.screen.Screen
#from pgzero.screen import Screen

WIDTH = 800
HEIGHT = 550
player_x = 500
player_y = 350

def draw():
    screen.blit(images.backdrop, (0,0))

pgzrun.go()