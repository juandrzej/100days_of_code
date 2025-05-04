# Create a letter using starting_letter.txt
# for each name in invited_names.txt
# Replace the [name] placeholder with the actual name.
# Save the letters in the folder "ReadyToSend".
    
with open("Input/Names/invited_names.txt") as names_file:
    names = names_file.read().splitlines()

with open("Input/Letters/starting_letter.txt") as letter_file:
    letter = letter_file.read()

for name in names:
    current_letter = letter.replace("[name]", name)
    with open(f"Output/ReadyToSend/{name}_letter.txt", mode="w") as curr_file:
        curr_file.write(current_letter)
