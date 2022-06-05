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

'''# creating squares
s1 = graphics.Shape(game_graphics, square)
change_to_square(s1, (255, 255, 255), (-500, 25, 250, 50, 0))
game_graphics.add_shape(s1)

# creating polygon
p1 = graphics.Shape(game_graphics, polygon)
change_to_polygon(p1, (200, 100, 0), [(0, 0, 0), (50, 0, 0), (50, 0, 50), (0, 0, 50)])
game_graphics.add_shape(p1)'''

# creating cube
c1 = graphics.Shape(game_graphics, cube)
change_to_cube(c1, (100, 0, 100), (100, 60, 20), (200, 100, 50))
game_graphics.add_shape(c1)

'''# line formula
lf1 = graphics.Shape(game_graphics, line_formula)
change_to_line_formula(lf1, (255, 200, 100), 0, 100, "20*sin(0.5*x)+0.1*(x**2)", "0.1*(x**2)", 1, width=5)
game_graphics.add_shape(lf1)'''


'''
s2 = graphics.Shape(game_graphics, square)
change_to_square(s2, (255, 255, 255), (400, 100, 50, 50))
game_graphics.add_shape(s2)'''

# creating axis
y_axis = graphics.Shape(game_graphics, line)
change_to_line(y_axis, (0, -100000, 0), (0, 100000, 0), (163, 85, 39))
game_graphics.add_shape(y_axis)

x_axis = graphics.Shape(game_graphics, line)
change_to_line(x_axis, (-100000, 0, 0), (100000, 0, 0), (163, 85, 39))
game_graphics.add_shape(x_axis)

z_axis = graphics.Shape(game_graphics, line)
change_to_line(z_axis, (0, 0, -1000), (0, 0, 1000), (163, 85, 39))
game_graphics.add_shape(z_axis)


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


# moving screen with mouse

def move_screen_with_mouse1():
    global first_mouse_pos, original_cam_pos
    first_mouse_pos = pygame.mouse.get_pos()
    original_cam_pos = (camera.x, camera.y)


def move_screen_mouse2():
    global first_mouse_pos, second_mouse_pos, original_cam_pos
    if pygame.mouse.get_pressed()[0]:
        second_mouse_pos = pygame.mouse.get_pos()
        camera.x = original_cam_pos[0] + -(second_mouse_pos[0] - first_mouse_pos[0])
        camera.y = original_cam_pos[1] + (second_mouse_pos[1] - first_mouse_pos[1])


move_screen_with_mouse1_input_func = ui.InputFunc("move screen with mouse 1", pygame.MOUSEBUTTONDOWN,
                                                  move_screen_with_mouse1)
move_screen_with_mouse2_looper = ui.Looper("move screen with mouse 2", move_screen_mouse2)

game_graphics.add_input_func(move_screen_with_mouse1_input_func)
game_graphics.add_looper(move_screen_with_mouse2_looper)

move_screen_looper = ui.Looper("move screen", move_screen)
game_graphics.add_looper(move_screen_looper)


# zooming
def zoom(event):
    global first_mouse_pos, second_mouse_pos
    if event.button == 4:
        camera.z -= 10
    elif event.button == 5:
        camera.z += 10


zoom_input_func = ui.InputFunc("zoom", pygame.MOUSEBUTTONDOWN, zoom, pass_event=True)
game_graphics.add_input_func(zoom_input_func)
