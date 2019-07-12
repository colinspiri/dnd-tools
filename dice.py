import random

def stringify_modifier(modifier):
    if modifier < 0:
        return str(modifier)
    else:
        return "+" + str(modifier)

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
            if "d" in modifier_text:
                modifier = roll(modifier_text)[2]
            else:
                modifier = int(modifier_text[modifier_text.find("+") + 1:])
        elif "-" in text:
            dice_text = text[:text.find("-")].strip()
            modifier_text = text[text.find("-") + 1:].strip()
            if "d" in modifier_text:
                modifier = roll(modifier_text)[2]
            else:
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

def show_attack(to_hit_modifier, damage_dice, damage_type = "", advantage = 0):
    # Input validation
    if not (advantage == 0 or advantage == 1 or advantage == -1):
        raise Exception("Advantage variable must be either 0 (nothing), 1 (advantage), or -1 (disadvantage).")

    # Advantage and to hit result
    if advantage == 0:
        rolls, _, to_hit_result = roll(str(to_hit_modifier))
        to_hit_roll = sum(rolls)
    else:
        rolls1 = roll("d20")[0]
        roll1 = sum(rolls1)
        rolls2 = roll("d20")[0]
        roll2 = sum(rolls2)
        all_rolls = rolls1 + rolls2
        if advantage == 1:
            to_hit_roll = roll1 if (roll1 > roll2) else roll2
            print("Rolled with advantage: " + str(all_rolls))
        elif advantage == -1:
            to_hit_roll = roll1 if (roll1 < roll2) else roll2
            print("Rolled with disadvantage: " + str(all_rolls))
        to_hit_result = to_hit_roll + to_hit_modifier
    print("To Hit: " + str(to_hit_result))

    # Critical miss
    if to_hit_roll == 1:
        print("CRITICAL FAILURE! MISSED ENTIRELY.")
        damage_result = 0
    else:
        # Damage
        damage_rolls, _, damage_result = roll(damage_dice)
        # Critical hit and extra damage
        if to_hit_roll == 20:
            if "+" in damage_dice:
                crit_dice = damage_dice[:damage_dice.rfind("+")]
            elif "-" in damage_dice:
                crit_dice = damage_dice[:damage_dice.rfind("-")]
            else:
                crit_dice = damage_dice
            crit_rolls, _, crit_result = roll(crit_dice)
            damage_result += crit_result
            print("CRITICAL HIT! INFLICTED EXTRA " + crit_dice + " DAMAGE.")
            print("Damage Rolls: " + str(damage_rolls) + " " + str(crit_rolls))
        else:
            print("Damage Rolls: " + str(damage_rolls))
        if damage_result < 0:
            damage_result = 0
        # Print damage and damage type
        if damage_type == "":
            print("Damage: " + str(damage_result))
        else:
            print("Damage: " + str(damage_result) + " (" + damage_type + ")")

    if to_hit_roll == 20:
        critical = True
    elif to_hit_roll == 1:
        critical = False
    else:
        critical = None
    return critical
def show_save(save_bonus, save_dc, advantage = 0):
    # Input validation
    if not (advantage == 0 or advantage == 1 or advantage == -1):
        raise Exception("Advantage variable must be either 0 (nothing), 1 (advantage), or -1 (disadvantage).")

    # Advantage and to hit result
    if advantage == 0:
        die_results, _, save_result = roll(str(save_bonus))
    else:
        rolls1 = roll("d20")[0]
        roll1 = sum(rolls1)
        rolls2 = roll("d20")[0]
        roll2 = sum(rolls2)
        all_rolls = rolls1 + rolls2
        if advantage == 1:
            roll_taken = roll1 if (roll1 > roll2) else roll2
            print("Rolled with advantage: " + str(all_rolls))
        elif advantage == -1:
            roll_taken = roll1 if (roll1 < roll2) else roll2
            print("Rolled with disadvantage: " + str(all_rolls))
        save_result = roll_taken + save_bonus

    # Print result
    if save_result >= int(save_dc):
        print("SUCCESS: " + str(save_result))
    else:
        print("FAILURE: " + str(save_result))

if __name__ == "__main__":
    while True:
        print()
        text = input("> ")
        show_roll(text)
