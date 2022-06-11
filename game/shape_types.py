import pygame
import graphics as graphics
import math
import parser
from math import *
import time


# rect needs to have a 5th argument for z position unless it is real
def change_to_square(shape, color, rect, real=False):
    shape.color = color
    shape.rect = rect
    shape.real = real


def draw_square(self):
    if self.real:
        rect = pygame.Rect(self.rect)
        if rect.right < 0 or rect.left > self.game_graphics.screen.width or rect.bottom < 0 or rect.top > self.game_graphics.screen.height:
            return False
        pygame.draw.rect(self.game_graphics.screen.screen, self.color, rect)
        return None
    pos = self.game_graphics.camera.vr_to_real((self.rect[0], self.rect[1], self.rect[4]))
    distance = self.rect[4] - self.game_graphics.camera.z
    if distance <= 0:
        return False
    magnify = self.game_graphics.camera.original_at/distance
    w = magnify*self.rect[2]
    h = magnify*self.rect[3]
    rect = pygame.Rect((pos[0], pos[1], w, h))
    if rect.right < 0 or rect.left > self.game_graphics.screen.width or rect.bottom < 0 or rect.top > self.game_graphics.screen.height:
        return False
    pygame.draw.rect(self.game_graphics.screen.screen, self.color, rect)


def move_square(self, movement):
    self.rect = (self.rect[0] + movement[0], self.rect[1] + movement[1], self.rect[2], self.rect[3])


square = graphics.Type("square", draw_square, move=move_square)
graphics.add_type(square)


# if not real, points should be (x, y, z)
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
    distance = (self.start_point[2] + self.end_point[2])/2 - self.game_graphics.camera.z

    if not end_point and start_point:
        try:
            z_slope = (self.start_point[2] - self.end_point[2])/(self.start_point[0] - self.end_point[0])
            z_b = self.start_point[2] - (self.start_point[0]*z_slope)
            z = self.game_graphics.camera.z + 1
            x = (z-z_b)/z_slope
        except ZeroDivisionError:
            z = self.game_graphics.camera.z + 1
            x = self.start_point[0]

        try:
            y_slope = (self.start_point[1] - self.end_point[1]) / (self.start_point[0] - self.end_point[0])
            y_b = self.start_point[1] - (self.start_point[0]*y_slope)
            y = x * y_slope + y_b
        except ZeroDivisionError:
            y = self.start_point[1]

        end_point = (x, y, z)
        end_point = self.game_graphics.camera.vr_to_real(end_point)

    if not start_point and end_point:
        #print(self.start_point, self.end_point)
        try:
            z_slope = (self.start_point[2] - self.end_point[2]) / (self.start_point[0] - self.end_point[0])
            z_b = self.start_point[2] - (self.start_point[0] * z_slope)
            z = self.game_graphics.camera.z + 1
            x = (z - z_b) / z_slope
        except ZeroDivisionError:
            z = self.game_graphics.camera.z + 1
            x = self.start_point[0]

        try:
            y_slope = (self.start_point[1] - self.end_point[1]) / (self.start_point[0] - self.end_point[0])
            y_b = self.start_point[1] - (self.start_point[0] * y_slope)
            y = x * y_slope + y_b
        except ZeroDivisionError:
            y = self.start_point[1]

        start_point = (x, y, z)
        #print(start_point)
        start_point = self.game_graphics.camera.vr_to_real(start_point)
        #print(start_point)

    if distance <= 0 or (not start_point or not end_point):
        return False

    magnify = self.game_graphics.camera.original_at / distance
    width = math.ceil(magnify * self.width)
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


# points need have a three arguments (x, y, z) unless it is real
def change_to_polygon(shape, color, points, outline=False, real=False):
    shape.color = color
    shape.points = points
    shape.outline = outline
    shape.real = real


def draw_polygon(self):
    if self.real:
        pygame.draw.polygon(self.game_graphics.screen.screen, self.color, self.points)
        return None
    new_points = []
    highest_x = 50
    lowest_x = 50
    highest_y = 50
    lowest_y = 50
    first = True
    start_time = time.time()
    for point in self.points:
        new_point = self.game_graphics.camera.vr_to_real(point)
        new_points.append(new_point)
        if new_point:
            if first:
                highest_x = new_point[0]
                lowest_x = new_point[0]
                highest_y = point[1]
                lowest_y = point[1]
                first = False

            elif point[0] > highest_x:
                highest_x = point[0]
            elif point[0] < lowest_x:
                lowest_x = point[0]

            if point[1] > highest_y:
                highest_y = point[1]
            elif point[1] < lowest_y:
                lowest_y = point[1]

    if highest_x < 0 or lowest_x > self.game_graphics.screen.width:
        return False
    elif highest_y < 0 or lowest_y > self.game_graphics.screen.height:
        return False

    counter = 0
    correct_points = []
    for point in self.points:
        calc_time = time.time()
        if not new_points[counter]:
            second_point = None
            if counter == 0:
                if not new_points[len(new_points)-1] and new_points[counter+1]:
                    second_point = self.points[counter+1]
                if new_points[len(new_points)-1] and not new_points[counter+1]:
                    second_point = self.points[len(new_points)-1]
            elif counter == len(new_points)-1:
                if not new_points[counter-1] and new_points[0]:
                    second_point = self.points[0]
                if new_points[counter-1] and not new_points[0]:
                    second_point = self.points[counter-1]
            else:
                if not new_points[counter-1] and new_points[counter+1]:
                    second_point = self.points[counter+1]
                if new_points[counter-1] and not new_points[counter+1]:
                    second_point = self.points[counter-1]

            if not second_point:
                counter += 1
                continue

            else:
                try:
                    z_slope = (point[2] - second_point[2]) / (point[0] - second_point[0])
                    z_b = point[2] - (point[0] * z_slope)
                    z = self.game_graphics.camera.z + 1
                    x = (z - z_b) / z_slope
                except ZeroDivisionError:
                    z = self.game_graphics.camera.z + 1
                    x = second_point[0]

                try:
                    y_slope = (point[1] - second_point[1]) / (point[0] - second_point[0])
                    y_b = point[1] - (point[0] * y_slope)
                    y = x * y_slope + y_b
                except ZeroDivisionError:
                    y = second_point[1]

                new_point = (x, y, z)
                new_point = self.game_graphics.camera.vr_to_real(new_point)
                final_time = time.time()
                correct_points.append(new_point)
                counter += 1
                continue

        else:
            new_point = self.game_graphics.camera.vr_to_real(point)
            final_time = time.time()
            correct_points.append(new_point)

        counter += 1

    better_points = []
    counter = 0
    for point in correct_points:
        new_point = None

        previous = None
        after = None

        if counter == 0:
            previous = correct_points[len(correct_points) - 1]
        else:
            previous = correct_points[counter - 1]

        if counter == len(correct_points) - 1:
            after = correct_points[0]
        else:
            after = correct_points[counter + 1]

        ignore_pre = False
        ignore_after = False
        x = None
        y = None

        if not point:
            continue

        if point[0] < 0:
            x = 0
            if not previous or previous[0] > self.game_graphics.screen.width:
                ignore_pre = True
            if not after or after[0] > self.game_graphics.screen.width:
                ignore_after = True
        elif point[0] > self.game_graphics.screen.width:
            x = self.game_graphics.screen.width
            if not previous or previous[0] < 0:
                ignore_pre = True
            if not after or after[0] < 0:
                ignore_after = True
        elif point[1] < 0:
            y = 0
            if not previous or previous[1] > self.game_graphics.screen.height:
                ignore_pre = True
            if not after or after[1] > self.game_graphics.screen.height:
                ignore_after = True
        elif point[1] > self.game_graphics.screen.height:
            y = self.game_graphics.screen.height
            if not previous or previous[1] < 0:
                ignore_pre = True
            if not after or after[1] < 0:
                ignore_after = True
        else:
            better_points.append(point)
            counter += 1
            continue

        if not y and y != 0:
            if previous and (not ((previous[0] < 0 or previous[0] > self.game_graphics.screen.width) or (previous[1] < 0 or previous[1] > self.game_graphics.screen.height)) or ignore_pre):
                try:
                    slope1 = (point[1] - previous[1]) / (point[0] - previous[0])
                    b1 = point[1] - point[0] * slope1
                    point1 = [x, x*slope1 + b1]
                except ZeroDivisionError:
                    point1 = [x, point[1]]

                better_points.append(point1)

            if point[0] > self.game_graphics.screen.width and point[1] > self.game_graphics.screen.height:
                new_point = [self.game_graphics.screen.width, self.game_graphics.screen.height]
            elif point[0] > self.game_graphics.screen.width and point[1] < 0:
                new_point = [self.game_graphics.screen.width, 0]
            elif point[0] < 0 and point[1] > self.game_graphics.screen.height:
                new_point = [0, self.game_graphics.screen.height]
            elif point[0] < 0 and point[1] < 0:
                new_point = [0, 0]
            if new_point:
                better_points.append(new_point)

            if after and (not ((after[0] < 0 or after[0] > self.game_graphics.screen.width) or (after[1] < 0 or after[1] > self.game_graphics.screen.height)) or ignore_after):
                try:
                    slope2 = (point[1] - after[1]) / (point[0] - after[0])
                    b2 = point[1] - point[0] * slope2
                    point2 = [x, x * slope2 + b2]
                except ZeroDivisionError:
                    point2 = [x, point[1]]

                better_points.append(point2)

        elif not x and x != 0:
            if previous and (not ((previous[0] < 0 or previous[0] > self.game_graphics.screen.width) or (previous[1] < 0 or previous[1] > self.game_graphics.screen.height)) or ignore_pre):
                try:
                    slope1 = (point[0] - previous[0]) / (point[1] - previous[1])
                    b1 = point[0] - point[1] * slope1
                    point1 = [y * slope1 + b1, y]
                except ZeroDivisionError:
                    point1 = [point[0], y]

                better_points.append(point1)

            if point[0] > self.game_graphics.screen.width and point[1] > self.game_graphics.screen.height:
                new_point = [self.game_graphics.screen.width, self.game_graphics.screen.height]
            elif point[0] > self.game_graphics.screen.width and point[1] < 0:
                new_point = [self.game_graphics.screen.width, 0]
            elif point[0] < 0 and point[1] > self.game_graphics.screen.height:
                new_point = [0, self.game_graphics.screen.height]
            elif point[0] < 0 and point[1] < 0:
                new_point = [0, 0]
            if new_point:
                better_points.append(new_point)

            if after and (not ((after[0] < 0 or after[0] > self.game_graphics.screen.width) or (after[1] < 0 or after[1] > self.game_graphics.screen.height)) or ignore_after):
                try:
                    slope2 = (point[0] - after[0]) / (point[1] - after[1])
                    b2 = point[0] - point[1] * slope2
                    point2 = [y * slope2 + b2, y]
                except ZeroDivisionError:
                    point2 = [point[0], y]

                better_points.append(point2)

        counter += 1

    correct_points = better_points

    if len(correct_points) >= 3:
        pygame.draw.polygon(self.game_graphics.screen.screen, self.color, correct_points)
        if self.outline:
            pygame.draw.polygon(self.game_graphics.screen.screen, (50, 50, 50), correct_points, width=2)


# movement: (x, y, z)
def move_polygon(self, movement):
    for i in range(len(self.points)):
        point = self.points[i]
        self.points[i] = (point[0] + movement[0], point[1] + movement[1], point[2] + movement[2])


polygon = graphics.Type("polygon", draw_polygon, move=move_polygon)
graphics.add_type(polygon)


# position: (x, y, z) back top left corner, dimensions (left to right, top to down, back to front)
def change_to_cube(shape, color, position, dimensions):
    shape.color = color
    shape.position = position
    shape.dimensions = dimensions

    shape.polygons = []

    # back
    p1 = graphics.Shape(shape.game_graphics, polygon)
    points = [
        position,
        (position[0] + dimensions[0], position[1], position[2]),
        (position[0] + dimensions[0], position[1] - dimensions[1], position[2]),
        (position[0], position[1] - dimensions[1], position[2])
    ]
    change_to_polygon(p1, color, points, outline=True)
    shape.polygons.append(p1)
    shape.back = p1

    # top
    p2 = graphics.Shape(shape.game_graphics, polygon)
    points = [
        position,
        (position[0] + dimensions[0], position[1], position[2]),
        (position[0] + dimensions[0], position[1], position[2] - dimensions[2]),
        (position[0], position[1], position[2] - dimensions[2])
    ]
    change_to_polygon(p2, color, points, outline=True)
    shape.polygons.append(p2)
    shape.top = p2

    # right
    p3 = graphics.Shape(shape.game_graphics, polygon)
    points = [
        (position[0] + dimensions[0], position[1], position[2]),
        (position[0] + dimensions[0], position[1], position[2] - dimensions[2]),
        (position[0] + dimensions[0], position[1] - dimensions[1], position[2] - dimensions[2]),
        (position[0] + dimensions[0], position[1] - dimensions[1], position[2])
    ]
    change_to_polygon(p3, color, points, outline=True)
    shape.polygons.append(p3)
    shape.right = p3

    # left
    p4 = graphics.Shape(shape.game_graphics, polygon)
    points = [
        (position[0], position[1], position[2]),
        (position[0], position[1], position[2] - dimensions[2]),
        (position[0], position[1] - dimensions[1], position[2] - dimensions[2]),
        (position[0], position[1] - dimensions[1], position[2])
    ]
    change_to_polygon(p4, color, points, outline=True)
    shape.polygons.append(p4)
    shape.left = p4

    # bottom
    p5 = graphics.Shape(shape.game_graphics, polygon)
    points = [
        (position[0], position[1] - dimensions[1], position[2]),
        (position[0] + dimensions[0], position[1] - dimensions[1], position[2]),
        (position[0] + dimensions[0], position[1] - dimensions[1], position[2] - dimensions[2]),
        (position[0], position[1] - dimensions[1], position[2] - dimensions[2])
    ]
    change_to_polygon(p5, color, points, outline=True)
    shape.polygons.append(p5)
    shape.bottom = p5

    # front
    p6 = graphics.Shape(shape.game_graphics, polygon)
    points = [
        (position[0], position[1], position[2] - dimensions[2]),
        (position[0] + dimensions[0], position[1], position[2] - dimensions[2]),
        (position[0] + dimensions[0], position[1] - dimensions[1], position[2] - dimensions[2]),
        (position[0], position[1] - dimensions[1], position[2] - dimensions[2])
    ]
    change_to_polygon(p6, color, points, outline=True)
    shape.polygons.append(p6)
    shape.front = p6


def draw_cube(self):
    # trying
    for poly in self.polygons:

        poly.draw()
    # back

    # top

    # right

    # left

    # bottom

    # front

    pass


cube = graphics.Type("cube", draw_cube)
graphics.add_type(cube)


def change_to_line_formula(shape, color, start_x, end_x, y_formula, z_formula, accuracy, width=1):
    shape.color = color
    shape.start_x = start_x
    shape.end_x = end_x
    shape.y_formula = y_formula
    shape.z_formula = z_formula
    shape.accuracy = accuracy

    shape.lines = []
    for i in range(start_x, end_x, accuracy):
        x = start_x + i
        y_code = parser.expr(y_formula).compile()
        z_code = parser.expr(z_formula).compile()
        start_pos = (x, eval(y_code), eval(z_code))
        x = start_x + i + accuracy
        end_pos = (x, eval(y_code), eval(z_code))

        l = graphics.Shape(shape.game_graphics, line)
        change_to_line(l, start_pos, end_pos, color, width=width)
        shape.lines.append(l)


def draw_line_formula(self):
    for lines in self.lines:
        lines.draw()


line_formula = graphics.Type("line formula", draw_line_formula)
graphics.add_type(line_formula)


def change_to_terrain(shape, color, position, width, length, y_formula, accuracy):
    shape.color = color
    shape.position = position
    shape.width = width
    shape.length = length
    shape.y_formula = y_formula
    shape.accuracy = accuracy

    shape.polygons = []

    for x in range(0, width-accuracy, accuracy):
        for z in range(0, length-accuracy, accuracy):
            try:
                y_code = parser.expr(y_formula).compile()
                y = position[1] + eval(y_code)
                point1 = [x+position[0], y+position[1], z+position[2]]

                x += accuracy
                y = position[1] + eval(y_code)
                point2 = [x+position[0], y+position[1], z+position[2]]

                z += accuracy
                y = position[1] + eval(y_code)
                point3 = [x+position[0], y+position[1], z+position[2]]

                x -= accuracy
                y = position[1] + eval(y_code)
                point4 = [x+position[0], y+position[1], z+position[2]]

                z -= accuracy

                # print(point1, point2, point3, point4)

                p = graphics.Shape(shape.game_graphics, polygon)
                shade = ((length-z)/(length-accuracy))
                change_to_polygon(p, (color[0]*shade, color[1]*shade, color[2]*shade), [point1, point2, point3, point4])
                shape.polygons.append(p)
            except ValueError:
                pass


def draw_terrain(self):
    counter = 0
    for poly in self.polygons:
        counter += 1
        self.polygons[-counter].draw()


terrain = graphics.Type("terrain", draw_terrain)
graphics.add_type(terrain)