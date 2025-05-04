import pandas
import turtle
from state_writer import StateWriter

screen = turtle.Screen()
screen.title("U.S. States Game")

image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

states_data = pandas.read_csv("50_states.csv")
states_list = states_data["state"].to_list()
x_list = states_data["x"].to_list()
y_list = states_data["y"].to_list()

states_dict = {}
for n in range(len(states_list)):
    states_dict.update({states_list[n]: (x_list[n], y_list[n])})

state_writer = StateWriter()
guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(f"{(len(guessed_states))}/50 States Correct",
                                    "What's another state's name?").title()

    if answer_state == "Exit":

        missing_states = [state for state in states_list if state not in guessed_states]

        df = pandas.DataFrame.from_dict(missing_states)
        df.to_csv("missing_states.csv")
        break

    if answer_state in states_list:
        state_writer.write_state(position=states_dict[answer_state], guessed_state=answer_state)
        guessed_states.append(answer_state)

