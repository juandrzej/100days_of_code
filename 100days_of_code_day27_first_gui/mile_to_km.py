import tkinter


def converter():
    value = round(float(input_field.get()) * 1.60934)
    value_label.config(text=f"{value}")


window = tkinter.Tk()
window.title("Mile to Km Converter")
window.minsize(width=400, height=200)
window.config(padx=100, pady=50)

input_field = tkinter.Entry(width=10)
input_field.grid(row=0, column=1)

miles_label = tkinter.Label(text="Miles")
miles_label.grid(row=0, column=2)

equal_label = tkinter.Label(text="is equal to")
equal_label.grid(row=1, column=0)

value_label = tkinter.Label(text=0)
value_label.grid(row=1, column=1)

km_label = tkinter.Label(text="Km")
km_label.grid(row=1, column=2)

button = tkinter.Button(text="Calculate", command=converter)
button.grid(row=2, column=1)


window.mainloop()
