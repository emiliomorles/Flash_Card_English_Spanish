from tkinter import *
import pandas
import random
import json

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ---------------------------- SHOW RANDOM ENGLISH WORDS ------------------------------- #

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/540_english_to_spanish.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")  # This is my dictionary of words

# ---------------------------- Functions ------------------------------- #


def next_card():
    """It changes the current card for a new random card"""
    if len(to_learn) == 0:
        print("the end")
        canvas.itemconfig(card_title, text="HAS TERMINADO 😎", fill="white")
        canvas.itemconfig(card_word, text="FELICIDADES 🎉", fill="white")

    else:

        global current_card, flip_timer  # There are two global variables
        window.after_cancel(flip_timer)  # There will cancel the global variable flip_timer
        current_card = random.choice(to_learn)
        canvas.itemconfig(card_title, text="Inglés", fill="black")  # The color changes back to black with 'fill='
        canvas.itemconfig(card_word, text=current_card["Inglés"], fill="black")
        canvas.itemconfig(card_background, image=card_front_img)  # The background changes back to 'background image'
        flip_timer = window.after(3000, func=flip_card)
        # New flip_timer in order to solve the bug that is caused by the first flip_timer


def flip_card():
    """It shows the meaning of the english word in spanish flipping the english card for a spanish card"""
    canvas.itemconfig(card_title, text="Español", fill="white")  # Change the color of the text with 'fill='
    canvas.itemconfig(card_word, text=current_card["Español"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)  # It changes the background image


def is_known():
    """It will remove the current_card because the user knows the meaning in spanish and it saves the file"""
    to_learn.remove(current_card)  # It removes the current_card
    print(len(to_learn))

    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    # In order to create the save file inside data I need to write "data/..."
    # index=False avoid to create numbers for the words every time the program stars again

    next_card()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)  # to flip the card after 3 seconds or 3000 milliseconds

# Words Label
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)  # 400 and 263 (half of 800 and 526)
card_title = canvas.create_text(400, 150, text="", font=('Arial', 40, "italic"), fill='black')
card_word = canvas.create_text(400, 263, text="", font=('Arial', 60, "bold"), fill='black')
canvas.grid(column=0, row=0, columnspan=2, sticky=EW)

#  Incorrect Answer Label (LEFT)
wrong_img = PhotoImage(file="images/wrong.png")
w_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
w_button.grid(column=0, row=1)

#  Correct Answer Label (RIGHT)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()
