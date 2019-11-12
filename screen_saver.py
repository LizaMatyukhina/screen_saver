import pygame
from random import random
from math import sqrt

SCREEN_SIZE = (1280, 720)


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):  # сумма векторов
        if other.is_vector(other):
            return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):  # разность векторов
        if other.is_vector(other):
            return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):  # умножение вектора на число
        if type(other) == int or type(other) == float:
            return Vector(self.x * other, self.y * other)
        elif other.is_vector(other):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError("IT'S ONLY ABOUT VECTORS!")

    def __len__(self, other):  # длинна вектора
        if other.is_vector(other):
            return sqrt(other.x * other.x + other.y * other.y)

    def int_pair(self):
        return tuple((int(self.x), int(self.y)))

    @staticmethod
    def is_vector(vector):
        if type(vector) == Vector:
            return True
        else:
            raise TypeError("IT'S ONLY ABOUT VECTORS!")


class Line:

    def __init__(self):
        self.points = []
        self.speeds = []

    def add(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for point in range(len(self.points)):
            self.points[point] += self.speeds[point]
            if self.points[point].x > SCREEN_SIZE[0] or self.points[point].x < 0:
                self.speeds[point] = Vector(- self.speeds[point].x, self.speeds[point].y)
            if self.points[point].y > SCREEN_SIZE[1] or self.points[point].y < 0:
                self.speeds[point] = Vector(self.speeds[point].x, -self.speeds[point].y)

    def draw_points(self, gameDisplay, points=None, style="points", width=4, color=(255, 255, 255)):
        if style == "line":
            for point_number in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, points[point_number].int_pair(),
                                 (points[point_number + 1].int_pair()), width)

        elif style == "points":
            for point in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (point.int_pair()), width)

    def speed_up(self, n):
        for s in range(len(self.speeds)):
            self.speeds[s] *= n

    def delete(self, ind):
        self.points.pop(ind)
        self.points.pop(ind)


class Joint(Line):

    def __init__(self, count):
        super(Joint, self).__init__()
        self.count = count

    def add_point(self, point, speed):
        super().add(point, speed)
        return self.get_joint()

    def set_points(self):
        super().set_points()
        return self.get_joint()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        result = []
        for i in range(count):
            result.append(self.get_point(base_points, i * alpha))
        return result

    def get_joint(self):
        if len(self.points) < 3:
            return []
        result = []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            pnt.append((self.points[i] + self.points[i + 1]) * 0.5)
            pnt.append(self.points[i + 1])
            pnt.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            result.extend(self.get_points(pnt, self.count))
        return result


def display_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["", ""])
    data.append([str(steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    points = []
    speeds = []
    show_help = False
    pause = False
    color_param = 0
    color = pygame.Color(0)

    joint = Joint(steps)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    joint = Joint(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_MINUS:
                    if len(joint.points) > 3:
                        joint.delete(-1)

                if event.key == pygame.K_UP:
                    joint.speed_up(2)
                if event.key == pygame.K_DOWN:
                    joint.speed_up(0.5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                joint.add_point(Vector(*event.pos), Vector(random() * 2, random() * 2))
        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        joint.draw_points(gameDisplay)
        joint.draw_points(gameDisplay, joint.get_joint(), "line", 4, color)
        if not pause:
            joint.set_points()
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
