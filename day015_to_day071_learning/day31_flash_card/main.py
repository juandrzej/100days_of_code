from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
current_card = {}


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
finally:
    cards_list = data.to_dict(orient="records")


def known_word():
    cards_list.remove(current_card)
    df = pandas.DataFrame(cards_list)
    df.to_csv("data/words_to_learn.csv", index=False, mode="w")
    generate_word()


def generate_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(cards_list)

    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")

    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

canvas_image = canvas.create_image(400, 263, image=card_front)
language = canvas.create_text(400, 150, text="Language", font=LANGUAGE_FONT)
word = canvas.create_text(400, 263, text="Word", font=WORD_FONT)

canvas.grid(row=0, column=0, columnspan=2)


wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=generate_word)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=known_word)
right_button.grid(row=1, column=1)

generate_word()

window.mainloop()
