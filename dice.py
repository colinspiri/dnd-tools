import random

def random_int(die_type):
    return random.randint(1, die_type)

def roll(text):
    # Rolling specified dice
    if "d" in text:
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
            rolls.append(random_int(die_type))
        result = sum(rolls) + modifier

        # Return output
        return rolls, modifier, result

    # Rolling 1d20 and a modifier
    elif "+" in text or "0" in text or "-" in text:
        # Get modifier and calculate result
        modifier = 0
        if "+" in text:
            modifier = int(text[text.find("+") + 1:])
        elif "-" in text:
            modifier = -int(text[text.find("-") + 1:])
        die_result = random_int(20)
        result = die_result + modifier

        # Return output
        return [die_result], modifier, result
    else:
        print("Cannot regonize input format. Please try again.")

def show_roll(input_text):
    if input_text == None or input_text == "":
        text = input("> ")
    else:
        text = input_text

    rolls, modifier, result = roll(text)

    if modifier < 0:
        print(str(rolls) + " (-" + str(abs(modifier)) + ")")
    else:
        print(str(rolls) + " (+" + str(modifier) + ")")
    print("Result: " + str(result))
    print()

if __name__ == "__main__":
    while True:
        text = input("> ")
        show_roll(text)
