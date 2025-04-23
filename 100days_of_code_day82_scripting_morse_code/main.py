morse_code: dict[str, str] = {
    "a": ". ___",
    "b": "___ . . .",
    "c": "___ . ___ .",
    "d": "___ . .",
}

def converter(base_list: list[str]) -> str:
    for char in base_list:
        pass

def main():
    user_input = input("Please give me a string to convert into Morse Code: ")
    user_input_list = list(user_input)
    print(user_input_list)

if __name__ == "__main__":
    main()
