from turtle import Turtle, Screen, clear

tim = Turtle()
screen = Screen()


def move_fd():
    tim.fd(10)


def move_bd():
    tim.backward(10)


def clockwise():
    tim.right(10)


def counter_clockwise():
    tim.left(10)


def reset_draw():
    tim.home()
    tim.clear()


screen.listen()

screen.onkey(move_fd, "w")
screen.onkey(move_bd, "s")
screen.onkey(clockwise, "d")
screen.onkey(counter_clockwise, "a")
screen.onkey(reset_draw, "c")

screen.exitonclick()
