import random

def random_int(die_type):
    result = random.randint(1, die_type)
    return result

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
        count_text = dice_text[:dice_text.find("d")]
        if not count_text.isdigit():
            count = 1
        else:
            count = int(count_text)
        die_type_text = dice_text[dice_text.find("d") + 1:]
        if die_type_text == "%":
            die_type = 100
        else:
            die_type = int(die_type_text)
        rolls = []
        for i in range(count):
            rolls.append(random_int(die_type))
        result = sum(rolls) + modifier

        # Return output
        return rolls, modifier, result

    # Rolling 1d20 and a modifier
    elif "+" in text or "0" in text or "-" in text or text.isdigit():
        # Get modifier and calculate result
        modifier = 0
        if "+" in text:
            modifier = int(text[text.find("+") + 1:])
        elif "-" in text:
            modifier = -int(text[text.find("-") + 1:])
        elif text.isdigit():
            modifier = int(text)
        die_result = random_int(20)
        result = die_result + modifier

        # Return output
        return [die_result], modifier, result
    else:
        print("Cannot regonize input format. Please try again.")
def show_roll(text):
    rolls, modifier, result = roll(text)

    if modifier < 0:
        print(str(rolls) + " (-" + str(abs(modifier)) + ")")
    else:
        print(str(rolls) + " (+" + str(modifier) + ")")
    print("Result: " + str(result))
    return rolls, modifier, result

def attack(to_hit_modifier, damage_dice):
    to_hit_tuple = roll(to_hit_modifier)
    to_hit_result = to_hit_tuple[2]
    # Critical hit on 20
    damage_tuple = roll(damage_dice)
    damage_result = damage_tuple[2]
    critical = None # None = normal, True = critical hit, False = critical failure
    natural_roll = sum(to_hit_tuple[0])
    if natural_roll == 20:
        damage_result += roll(damage_dice)[2]
        critical = True
    elif natural_roll == 1:
        critical = False
        damage_result = 0
    return to_hit_result, damage_result, critical
def show_attack(to_hit_modifier, damage_dice):
    to_hit_result, damage_result, critical = attack(to_hit_modifier, damage_dice)

    print("To Hit: " + str(to_hit_result))
    if critical == True:
        print("CRITICAL HIT! DOUBLE DAMAGE INFLICTED.")
    elif critical == False:
        print("CRITICAL FAILURE! MISSED ENTIRELY.")
    print("Damage: " + str(damage_result))
    return to_hit_result, damage_result, critical

def save(save_bonus, save_dc):
    die_result, modifier, saving_throw = roll(save_bonus)
    save_success = saving_throw >= int(save_dc)
    return save_success, saving_throw
def show_save(save_bonus, save_dc):
    save_success, saving_throw = save(save_bonus, save_dc)
    if save_success:
        print("Save successful with " + str(saving_throw) + ".")
    else:
        print("Save failed with " + str(saving_throw) + ".")
    return save_success, saving_throw

if __name__ == "__main__":
    while True:
        text = input("> ")
        elements = text.split()
        show_save(elements[0], elements[1])
