import math


def lcm(a, b):
    return int((a*b)/math.gcd(a, b))


def rotate_point(point2d, rotation, rotation_center=(0, 0)):
    # print(rotation_center)
    x = (point2d[0]-rotation_center[0])*math.cos(math.radians(rotation)) - (point2d[1] - rotation_center[1])*math.sin(math.radians(rotation)) + rotation_center[0]
    y = (point2d[0] - rotation_center[0]) * math.sin(math.radians(rotation)) + (point2d[1] - rotation_center[1]) * math.cos(math.radians(rotation)) + rotation_center[1]
    return x, y


def calculate_parallel_distant(center, point, angle):
    angle = angle%180
    x = 0
    y = 0
    slope = round(math.tan(math.radians(angle)), 3)
    if angle == 90:
        x = center[0]
    elif angle == 0:
        y = center[1]
    try:
        e_b = center[1] - (-center[0]/slope)
    except ZeroDivisionError:
        e_b = center[1]
    p_b = point[1] - (point[0]*slope)

    if not x:
        x = -(slope * (p_b - e_b))/(slope**2+1)
        if angle == 0:
            x = point[0]
    if not y:
        y = slope*x + p_b
        if angle == 90:
            y = point[1]

    d = math.sqrt((point[0] - x)**2 + (point[1] - y)**2)
    return d


#print(calculate_parallel_distant((-400, 0), (12, 0), 0))