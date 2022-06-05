import graphics
import manager
from shape_types import *
import pygame
import user_input as ui


# setting up a game_graphics
screen = graphics.Screen(1000, 700)
game_graphics = graphics.GameGraphics(screen, None)
camera = graphics.Camera(0, 10, -400, game_graphics, original_at=400)
game_graphics.camera = camera
graphics.add_game_graphics(game_graphics)

game_graphics.name = "first"

# setting up the screen and main graphics
manager.game_loop.make_screen(1000, 700)
manager.game_loop.set_main_game_graphics(game_graphics)

# creating squares
s1 = graphics.Shape(game_graphics, square)
change_to_square(s1, (255, 255, 255), (-500, 25, 250, 50, 0))
game_graphics.add_shape(s1)

# creating polygon
p1 = graphics.Shape(game_graphics, polygon)
change_to_polygon(p1, (200, 100, 0), [(0, 0, 0), (50, 0, 0), (50, 0, 50), (0, 0, 50)])
game_graphics.add_shape(p1)

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



# moving screen with mouse
speed = 10
first_mouse_pos = (0, 0)
second_mouse_pos = (0, 0)
original_cam_pos = (0, 0)


def move_screen():
    global speed
    global camera
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        camera.move((speed, 0))
    if keys[pygame.K_LEFT]:
        camera.move((-speed, 0))
    if keys[pygame.K_UP]:
        camera.move((0, speed))
    if keys[pygame.K_DOWN]:
        camera.move((0, -speed))


move_screen_looper = ui.Looper("move screen", move_screen)
game_graphics.add_looper(move_screen_looper)


