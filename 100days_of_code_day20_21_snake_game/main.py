import time
from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard

screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")


game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    # Detect collision with food
    if snake.head.distance(food) < 15:
        snake.extend()
        scoreboard.add_score()
        food.refresh()

    # Detect collision with wall
    x_corr = snake.head.xcor()
    y_corr = snake.head.ycor()
    if x_corr > 280 or x_corr < -280 or y_corr > 280 or y_corr < -280:
        scoreboard.reset()
        snake.reset()

    # Detect collision with tail
    for part in snake.snake_parts[1:]:
        if snake.head.distance(part) < 10:
            scoreboard.reset()
            snake.reset()


screen.exitonclick()
