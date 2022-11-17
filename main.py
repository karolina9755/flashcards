from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
WORDS_PATH = "data/words_to_learn.csv"
ORIGINAL_PATH = "data/french_words.csv"
current_card = {}
words_to_learn = {}

def import_words():
    global words_to_learn
    try:
        data = pandas.read_csv(WORDS_PATH)
    except FileNotFoundError:
        data_frame = pandas.read_csv(ORIGINAL_PATH)
        words_to_learn = data_frame.to_dict(orient="records")
    else:
        words_to_learn = data.to_dict(orient="records")
    print(words_to_learn)
    print(len(words_to_learn))
    if not words_to_learn:
        data_frame = pandas.read_csv(ORIGINAL_PATH)
        words_to_learn = data_frame.to_dict(orient="records")


def word_known():
    global words_to_learn, current_card
    words_to_learn.remove(current_card)
    data = pandas.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

def word_unknown():
    next_card()

def next_card():
    global flip_timer
    global words_to_learn
    global current_card
    window.after_cancel(flip_timer)
    try:
        current_card = random.choice(words_to_learn)
    except IndexError:
        flashcard.itemconfig(card_background, image=front_image)
        flashcard.itemconfig(language, text="Well done!", fill="black")
        flashcard.itemconfig(word, text="No more words to learn", fill="black", font=("Ariel", 40, "bold"))
        window.after(5000)
        window.quit()
    else:
        flashcard.itemconfig(card_background, image=front_image)
        flashcard.itemconfig(word, text=current_card["French"], fill="black")
        flashcard.itemconfig(language, text="French", fill="black")
        flip_timer = window.after(3000, func=flip_card)

def flip_card():
    flashcard.itemconfig(card_background, image=back_image)
    flashcard.itemconfig(word, text=current_card["English"], fill="white")
    flashcard.itemconfig(language, text="English", fill="white")


window = Tk()
window.minsize(height=526, width=800)
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")

right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

flashcard = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = flashcard.create_image(400, 263, image=front_image)
language = flashcard.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
word = flashcard.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
flashcard.grid(row=0, column=0, columnspan=2)

unknown_button = Button(image=wrong_image, highlightthickness=0, command=word_unknown)
unknown_button.grid(row=1, column=0)

known_button = Button(image=right_image, highlightthickness=0, command=word_known)
known_button.grid(row=1, column=1)



import_words()
next_card()



window.mainloop()
