import tkinter


def button_clicked():
    print("I got clicked")
    # my_label.config(text="button got clicked")
    my_label.config(text=input_f.get())


# main window
window = tkinter.Tk()
window.title("My first GUI program")
window.minsize(width=500, height=300)
window.config(padx=20, pady=20)

# label
my_label = tkinter.Label(text="I am a Label", font=("Arial", 24, "bold"))
# my_label["text"] = "newtext"
my_label.config(text="newtext")
# my_label.pack()
# my_label.place(x=100, y=200)
my_label.grid(column=0, row=0)


# button
button = tkinter.Button(text="Click me", command=button_clicked)
# button.pack()
button.grid(column=1, row=1)

# 2nd button
new_button = tkinter.Button(text="new button", command=button_clicked)
# button.pack()
new_button.grid(column=2, row=0)

# entry
input_f = tkinter.Entry(width=10)
# input_f.pack()
input_f.grid(column=3, row=2)




window.mainloop()
