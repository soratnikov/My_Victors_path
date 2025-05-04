import pgzero
import pgzrun
from pgzero.loaders import images

screen: pgzero.screen.Screen


WIDTH = 800
HEIGHT = 600
player_x = 500
player_y = 550

def draw():
    screen.blit(images.backdrop, (0,0))

pgzrun.go()