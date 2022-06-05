import pygame
import graphics as graphics
import math


# rect needs to have a 5th argument for z position unless it is real
def change_to_square(shape, color, rect, real=False):
    shape.color = color
    shape.rect = rect
    shape.real = real


def draw_square(self):
    if self.real:
        pygame.draw.rect(self.game_graphics.screen.screen, self.color, self.rect)
        return None
    pos = self.game_graphics.camera.vr_to_real((self.rect[0], self.rect[1]), z=self.rect[4])
    distance = self.rect[4] - self.game_graphics.camera.z
    if distance <= 0:
        return False
    magnify = self.game_graphics.camera.original_at/distance
    w = magnify*self.rect[2]
    h = magnify*self.rect[3]
    pygame.draw.rect(self.game_graphics.screen.screen, self.color, (pos[0], pos[1], w, h))


def move_square(self, movement):
    self.rect = (self.rect[0] + movement[0], self.rect[1] + movement[1], self.rect[2], self.rect[3])


square = graphics.Type("square", draw_square, move=move_square)
graphics.add_type(square)


def change_to_line(shape, start_point, end_point, color, width=1, real=False):
    shape.start_point = start_point
    shape.end_point = end_point
    shape.color = color
    shape.width = width
    shape.real = real


def draw_line(self):
    if self.real:
        pygame.draw.line(self.game_graphics.screen.screen, self.color, self.start_point, self.end_point, self.width)
        return None
    start_point = self.game_graphics.camera.vr_to_real(self.start_point)
    end_point = self.game_graphics.camera.vr_to_real(self.end_point)
    width = math.ceil(self.game_graphics.camera.zoom * self.width)
    pygame.draw.line(self.game_graphics.screen.screen, self.color, start_point, end_point, width)


def move_line(self, movement):
    self.start_point = (self.start_point[0] + movement[0], self.start_point[1] + movement[1])
    self.end_point = (self.end_point[0] + movement[0], self.end_point[1] + movement[1])


line = graphics.Type("line", draw_line, move=move_line)
graphics.add_type(line)


def change_to_circle(shape, center, radius, color, real=False):
    shape.center = center
    shape.radius = radius
    shape.color = color
    shape.real = real


def draw_circle(self):
    if self.real:
        pygame.draw.circle(self.game_graphics.screen.screen, self.color, self.center, self.radius)
        return None
    center = self.game_graphics.camera.vr_to_real(self.center)
    radius = self.game_graphics.camera.zoom * self.radius
    pygame.draw.circle(self.game_graphics.screen.screen, self.color, center, radius)


def move_circle(self, movement):
    self.center = (self.center[0] + movement[0], self.center[1] + movement[1])


circle = graphics.Type("circle", draw_circle, move=move_circle)
graphics.add_type(circle)


# position: (x, y, z) back top left corner, dimensions (left to right, top to down, back to front)
def change_to_cube(shape, color, position, dimensions):
    shape.color = color
    shape.position = position
    shape.dimensions = dimensions

    shape.squares = []

    # back
    s1 = graphics.Shape(shape.game_graphics, square)
    change_to_square(s1, (255, 255, 255), ([position[0], position[1]], 25, 50, 50))
    shape.squares.append(s1)

    # top

    # right

    # left

    # front


def draw_cube(self):

    # back

    # top

    # right

    # left

    # front

    pass
