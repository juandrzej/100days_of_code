from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
TICKS = ""
TIMER = None


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global TIMER, TICKS, REPS
    window.after_cancel(TIMER)
    timer_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    TICKS = ""
    REPS = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global REPS
    REPS += 1

    work_sec = WORK_MIN * 60
    break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    print(REPS)
    if REPS % 2 == 1:
        timer_label.config(text="Work", fg=GREEN)
        count_down(work_sec)
    elif REPS % 8 == 0:
        timer_label.config(text="Break", fg=RED)
        count_down(long_break_sec)
    else:
        timer_label.config(text="Break", fg=PINK)
        count_down(break_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global TICKS, TIMER
    count_min = count // 60
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        TIMER = window.after(1000, count_down, count - 1)
    else:
        if REPS % 2 == 1:
            TICKS += "✔"
            tick_label.config(text=TICKS)
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
image = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=image)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 32, "bold"))
canvas.grid(row=1, column=1)

timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 32))
timer_label.grid(row=0, column=1)

start_button = Button(text="Start", bg="white", font=(FONT_NAME, 10), command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", bg="white", font=(FONT_NAME, 10), command=reset_timer)
reset_button.grid(row=2, column=2)

tick_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20))
tick_label.grid(row=3, column=1)

window.mainloop()
