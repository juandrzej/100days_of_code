from turtle import Turtle
DISTANCE = 20


class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.color("white")
        self.penup()
        self.shape("square")
        self.shapesize(5, 1)
        self.goto(position)

    def move_up(self):
        new_y = self.ycor() + DISTANCE
        self.goto(self.xcor(), new_y)

    def move_down(self):
        new_y = self.ycor() - DISTANCE
        self.goto(self.xcor(), new_y)

