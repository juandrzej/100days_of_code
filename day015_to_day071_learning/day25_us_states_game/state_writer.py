from turtle import Turtle


class StateWriter(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()

    def write_state(self, position, guessed_state):
        self.goto(position)
        self.write(f"{guessed_state}", align="center", font=("Arial", 8, "normal"))
