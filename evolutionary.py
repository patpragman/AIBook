import random
from math import sqrt
from debris_field import Field
import turtle
turtle.delay(0)
t = turtle.Turtle()
t.speed(0)
t.hideturtle()

x_width = 250
y_width = 250

t.write("start")
t.pu()
t.setposition(x_width, y_width)
t.pd()
t.write("finish")
t.pu()
t.setposition(0, 0)

obstacle_field = Field(x_width, y_width, t)


for a in range(30, 60):
    for b in range(30, 56):
        obstacle_field.add_rock(a, b)

for a in range(100, 200):
    for b in range(30, 56):
        obstacle_field.add_rock(a, b)

for a in range(20, 200):
    for b in range(80, 90):
        obstacle_field.add_rock(a, b)

instructions = ["up", "down", "left", "right", "upright", "upleft", "downright", "downleft"]
starting_point = (0, 0)
ending_point = (x_width, y_width)
max_iterations = int(sqrt(x_width**2 + y_width**2)//1)*2

class PathWay:

    def __init__(self,
                 dna=random.choices(instructions, k=max_iterations),
                 mutations=10,
                 starting_point=(0, 0),
                 ending_point=(x_width, y_width),
                 field=obstacle_field):
        self.dna = dna
        self.mutations = mutations
        self.field = field

        self.starting_point = starting_point
        self.cur_x, self.cur_y = self.starting_point
        self.ending_point = ending_point

    def mutate(self):
        mutations = random.choices(range(0, len(self.dna)), k=self.mutations)

        for mutation in mutations:
            self.dna[mutation] = random.choice(instructions)

    def evaluate_fitness(self, draw=False):
        self.cur_x, self.cur_y = self.starting_point
        for i in self.dna:
            prev_x, prev_y = self.cur_x, self.cur_y

            if i == "left":
                self.cur_x -= 1
            elif i == "right":
                self.cur_x += 1
            elif i == "up":
                self.cur_y += 1
            elif i == "down":
                self.cur_y -= 1
            elif i == "upright":
                self.cur_y += 1
                self.cur_x += 1
            elif i == "upleft":
                self.cur_y += 1
                self.cur_x -= 1
            elif i == "downright":
                self.cur_y -= 1
                self.cur_x += 1
            elif i == "downleft":
                self.cur_y -= 1
                self.cur_y -= 1

            try:
                if self.field.coords[self.cur_x - 1][self.cur_y - 1]:
                    # if there's a rock there... go back
                    self.cur_x = prev_x
                    self.cur_y = prev_y
            except IndexError:
                # this threw an error because you're outside of the area you can play in
                self.cur_x = prev_x
                self.cur_y = prev_y
                return x_width*y_width

            if draw:
                t.setposition(self.cur_x, self.cur_y)
                t.pendown()
                t.dot(1, "red")  # drawing the pixel.
                t.pu()

        goal_x, goal_y = self.ending_point
        return sqrt((goal_y - self.cur_y)**2 + (goal_x - self.cur_x)**2)


path = PathWay()
fitness = path.evaluate_fitness()
i = 0
while fitness >= 1:
    i += 1
    old_dna = path.dna.copy()
    path.mutate()
    new_fitness = path.evaluate_fitness()
    if new_fitness <= fitness:
        # if you got better results, keep going!
        fitness = new_fitness
        continue
    else:
        # otherwise restore the dna to the original
        path.dna = old_dna

path.evaluate_fitness(True)

print(fitness, i)
print(path.dna)
turtle.exitonclick()