# import colorgram
#
# colors = colorgram.extract('image.jpg',30)
# color_list = []
# for color in colors:
#     red = color.rgb.r
#     green = color.rgb.g
#     blue = color.rgb.b
#     color_list.append((red,green,blue))
#
# print(color_list)

final_list=[(141, 163, 182), (14, 119, 185), (206, 138, 168), (199, 175, 9), (240, 213, 62), (220, 156, 97),
            (150, 17, 34), (122, 72, 100), (13, 143, 53), (74, 29, 35), (59, 34, 31), (204, 67, 26), (226, 170, 199),
            (242, 80, 27), (16, 172, 189), (34, 176, 93), (2, 114, 63), (247, 214, 2), (114, 188, 142), (181, 95, 111),
            (188, 182, 211), (40, 39, 46), (157, 207, 217), (229, 173, 162), (162, 208, 181), (118, 117, 163)]

import turtle as t
import random

timmy = t.Turtle()
screen = t.Screen()

t.colormode(255)
timmy.penup()
timmy.hideturtle()
timmy.speed("fastest")

for y in range(-5,5):
    timmy.goto(-250,y*50)
    for x in range(10):
        timmy.dot(20,random.choice(final_list))
        timmy.fd(50)





screen.exitonclick()