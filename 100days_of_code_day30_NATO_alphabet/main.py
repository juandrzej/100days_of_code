import pandas

data = pandas.read_csv("nato_phonetic_alphabet.csv")

my_dict = {row.letter: row.code for (index, row) in data.iterrows()}


def generate_phonetic():
    user_input = input("Write a word:").upper()
    try:
        code_words = [my_dict[letter] for letter in user_input]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic()
    else:
        print(code_words)


generate_phonetic()
