# 1. The lenght of a dot in one unit.
# 2. A dash is three units.
# 3. The space between parts of the same letter is one unit.
morse_code: dict[str, str] = {
    "a": ". ___",
    "b": "___ . . .",
    "c": "___ . ___ .",
    "d": "___ . .",
    "e": ".",
    "f": ". . ___ .",
    "g": "___ ___ .",
    "h": ". . . .",
    "i": ". .",
    "j": ". ___ ___ ___",
    "k": "___ . ___",
    "l": ". ___ . .",
    "m": "___ ___",
    "n": "___ .",
    "o": "___ ___ ___",
    "p": ". ___ ___ .",
    "q": "___ ___ . ___",
    "r": ". ___ .",
    "s": ". . .",
    "t": "___",
    "u": ". . ___",
    "v": ". . . ___",
    "w": ". ___ ___",
    "x": "___ . . ___",
    "y": "___ . ___ ___",
    "z": "___ ___ . .",
    "1": ". ___ ___ ___ ___",
    "2": ". . ___ ___ ___",
    "3": ". . . ___ ___",
    "4": ". . . . ___",
    "5": ". . . . .",
    "6": "___ . . . .",
    "7": "___ ___ . . .",
    "8": "___ ___ ___ . .",
    "9": "___ ___ ___ ___ .",
    "0": "___ ___ ___ ___ ___",
}

invalid_characters: set[str] = set()


def word_converter(word: str) -> str:
    """Function to convert a word to Morse Code."""
    converted_characters: list = []
    for char in word:
        try:
            converted_characters.append(morse_code[char.lower()])
        except KeyError:
            invalid_characters.add(char)
    # 4. The space between letters is three units.
    return "   ".join(converted_characters)


def morse_converter(input: str) -> str:
    """Function to take input string and convert it to Morse Code string."""
    words: list[str] = input.split()
    converted_words: list[str] = []
    for word in words:
        converted_words.append(word_converter(word))
    # 5. The space betwen words is seven units.
    return "       ".join(converted_words)


def main():
    user_input = input("Please give me a string to convert into Morse Code: ")
    converted_input: str = morse_converter(user_input)
    print(
        f"Please see the below string after convertion to Morse Code: \n{converted_input}"
    )
    if invalid_characters:
        print(
            f"The provided invalid characters have been skipped: {', '.join(invalid_characters)}."
        )


if __name__ == "__main__":
    main()
