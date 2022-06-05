import graphics
import manager
from shape_types import *
import pygame
import user_input as ui


# setting up a game_graphics
screen = graphics.Screen(1000, 700)
game_graphics = graphics.GameGraphics(screen, None)
camera = graphics.Camera(0, 0, -30, game_graphics, original_at=20)
game_graphics.camera = camera
graphics.add_game_graphics(game_graphics)

game_graphics.name = "first"

# setting up the screen and main graphics
manager.game_loop.make_screen(1000, 700)
manager.game_loop.set_main_game_graphics(game_graphics)

# creating squares
s1 = graphics.Shape(game_graphics, square)
change_to_square(s1, (255, 255, 255), (-500, 25, 500, 50, 0))
game_graphics.add_shape(s1)
'''
s2 = graphics.Shape(game_graphics, square)
change_to_square(s2, (255, 255, 255), (400, 100, 50, 50))
game_graphics.add_shape(s2)'''

'''# creating axis
y_axis = graphics.Shape(game_graphics, line)
change_to_line(y_axis, (0, -100000), (0, 100000), (163, 85, 39))
game_graphics.add_shape(y_axis)

x_axis = graphics.Shape(game_graphics, line)
change_to_line(x_axis, (-100000, 0), (100000, 0), (163, 85, 39))
game_graphics.add_shape(x_axis)'''
