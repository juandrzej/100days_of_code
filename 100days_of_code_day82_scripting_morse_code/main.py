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
}

def converter(base_list: list[str]) -> str:
    converted_list: list = []
    for char in base_list:
        if char in morse_code:
            converted_list.append(morse_code[char])
    
    return "".join(converted_list)

def main():
    user_input = input("Please give me a string to convert into Morse Code: ")
    user_input_list = list(user_input)
    print(user_input_list)
    converted_input: str = converter(user_input_list)
    print(converted_input)

if __name__ == "__main__":
    main()
