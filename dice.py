import random

def roll(die_type):
    return random.randint(1, die_type)

def roll_from_input(input_text):
    text = None
    if input_text == None or input_text == "":
        text = input("> ")
    else:
        text = input_text

    # Rolling specified dice
    if "d" in text:
        dice_text = None
        modifier = None
        # Parse text and separate dice from modifier
        if "+" in text:
            dice_text = text[:text.find("+")].strip()
            modifier_text = text[text.find("+") + 1:].strip()
            modifier = int(modifier_text[modifier_text.find("+") + 1:])
        elif "-" in text:
            dice_text = text[:text.find("-")].strip()
            modifier_text = text[text.find("-") + 1:].strip()
            modifier = -int(modifier_text[modifier_text.find("-") + 1:])
        else:
            dice_text = text
            modifier = 0

        # Roll dice and calculate result
        count = int(dice_text[:dice_text.find("d")])
        die_type = int(dice_text[dice_text.find("d") + 1:])
        rolls = []
        for i in range(count):
            rolls.append(roll(die_type))
        result = sum(rolls) + modifier

        # Print output
        print(rolls)
        print(str(sum(rolls)) + " + " + str(modifier))
        print("Result: " + str(result))

    # Rolling 1d20 and a modifier
    elif "+" in text or "0" in text or "-" in text:
        # Get modifier and calculate result
        modifier = 0
        if "+" in text:
            modifier = int(text[text.find("+") + 1:])
        elif "-" in text:
            modifier = -int(text[text.find("-") + 1:])
        die_result = roll(20)
        result = die_result + modifier

        # Print output
        print(str(die_result) + " + " + str(modifier))
        print("Result: " + str(result))
    else:
        print("Cannot regonize input format. Please try again.")
    print()

if __name__ == "__main__":
    while True:
        text = input("> ")
        roll_from_input(text)
