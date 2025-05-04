import turtle as t
import random

t.colormode(255)
screen = t.Screen()
timmy = t.Turtle()
timmy.shape("turtle")
timmy.color("DarkOrchid4")

def drawing_color():
    r = random.randrange(0,255,10)
    g = random.randrange(0, 255, 10)
    b = random.randrange(0, 255, 10)
    return (r,g,b)

# part1
# for shape in range(3,11):
#     timmy.pencolor(drawing_color())
#     angle = 360 / shape
#     for side in range(shape):
#         timmy.forward(50)
#         timmy.right(angle)

# part2
# timmy.speed("fastest")
# timmy.width(10)
# for i in range(500):
#     timmy.pencolor(drawing_color())
#     timmy.forward(20)
#     angle = random.randrange(0,360,90)
#     timmy.right(angle)

# part3
timmy.speed("fastest")
for i in range(100):
    timmy.pencolor(drawing_color())
    timmy.circle(100)
    timmy.setheading(3.6 * i)

screen.exitonclick()