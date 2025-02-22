import tkinter
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list.extend([choice(symbols) for _ in range(randint(2, 4))])
    password_list.extend([choice(numbers) for _ in range(randint(2, 4))])

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = website_entry.get()
    username = user_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": username,
            "password": password
        }
    }

    if len(website) < 1 or len(password) < 1:
        tkinter.messagebox.showwarning(title="Oops", message="You have left some empty lines!")
        return

    try:
        with open("data.json", mode="r") as data_file:
            # reading data
            data = json.load(data_file)
            # updating data
            data.update(new_data)
    except FileNotFoundError:
        data = new_data
    finally:
        with open("data.json", mode="w") as data_file:
            # saving updated data
            json.dump(data, data_file, indent=4)

    website_entry.delete(0, tkinter.END)
    password_entry.delete(0, tkinter.END)


# ---------------------------- SEARCH ------------------------------- #
def search():
    website = website_entry.get()

    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        tkinter.messagebox.showerror(title="Error", message="No Data File Found")
    else:
        if website in data:
            tkinter.messagebox.showinfo(title=website,
                                        message=f"Email: {data[website]["email"]}\n"
                                                f"Password: {data[website]["password"]}")
        else:
            tkinter.messagebox.showinfo(title="No data", message=f"No details for the {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tkinter.Canvas(width=200, height=200)
image = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)

website_label = tkinter.Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = tkinter.Entry(width=28)
website_entry.grid(row=1, column=1)
website_entry.focus()

search_button = tkinter.Button(text="Search", width=15, command=search)
search_button.grid(row=1, column=2)

user_label = tkinter.Label(text="Email/Username:")
user_label.grid(row=2, column=0)

user_entry = tkinter.Entry(width=47)
user_entry.grid(row=2, column=1, columnspan=2)
user_entry.insert(0, "test@gmail.com")

password_label = tkinter.Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = tkinter.Entry(width=28)
password_entry.grid(row=3, column=1)

password_button = tkinter.Button(text="Generate Password", command=generate_password)
password_button.grid(row=3, column=2)

add_button = tkinter.Button(text="Add", width=40, command=add_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
