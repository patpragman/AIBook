import random


class Field:

    def __init__(self, x, y, turtle=None):
        self.coords = [[0] * y for i in range(x)]
        self.turtle = turtle

    def add_rock(self, x, y):
        self.coords[x][y] = 1
        self.turtle.setposition(x, y)
        self.turtle.pendown()
        self.turtle.dot(1, "black")  # drawing the pixel.
        self.turtle.penup()

