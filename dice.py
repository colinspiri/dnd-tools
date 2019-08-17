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
def show_advantage_roll(advantage):
    # Input validation
    if not (advantage == 0 or advantage == 1 or advantage == -1):
        raise Exception("Advantage variable must be either 0 (nothing), 1 (advantage), or -1 (disadvantage).")

    rolls1 = [random_int(20)]
    roll1 = sum(rolls1)
    rolls2 = [random_int(20)]
    roll2 = sum(rolls2)
    rolls = rolls1 + rolls2
    if advantage == 1:
        result = roll1 if (roll1 > roll2) else roll2
        print("Rolled with advantage: " + str(rolls))
    elif advantage == -1:
        result = roll1 if (roll1 < roll2) else roll2
        print("Rolled with disadvantage: " + str(rolls))
    return result
def show_roll(text, advantage = 0):
    rolls, modifier, result = roll(text)

    if advantage is not 0:
        pre_modifier_result = show_advantage_roll(advantage)
        result = pre_modifier_result + modifier
        rolls = [pre_modifier_result]

    print(str(rolls) + " (" + stringify_modifier(modifier) + ")")
    print("Result: " + str(result))
    return rolls, modifier, result

def show_attack(to_hit_modifier, damage_dice, damage_type = "", advantage = 0):
    # To hit result
    if advantage is 0:
        rolls, _, to_hit_result = roll(str(to_hit_modifier))
        to_hit_roll = sum(rolls)
    else:
        to_hit_roll = show_advantage_roll(advantage)
        to_hit_result = to_hit_roll + to_hit_modifier
    print("To Hit: " + str(to_hit_result))

    # Critical miss
    if to_hit_roll == 1:
        print("CRITICAL FAILURE! MISSED ENTIRELY.")
        damage_result = 0
    elif damage_dice == None:
        if to_hit_roll == 20:
            print("CRITICAL HIT!")
    else:
        # Damage
        damage_rolls, _, damage_result = roll(damage_dice)
        damage_text = "Damage: "

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
            damage_text += str(damage_rolls) + " " + str(crit_rolls)
        else:
            damage_text += str(damage_rolls)
        if damage_result < 0:
            damage_result = 0
        # Print damage and damage type
        damage_text += "; " + str(damage_result)
        if not damage_type == "":
            damage_text += " (" + damage_type + ")"
        print(damage_text)

    if to_hit_roll == 20:
        critical = True
    elif to_hit_roll == 1:
        critical = False
    else:
        critical = None
    return critical
def show_save(save_bonus, save_dc, advantage = 0):
    # To hit result
    if advantage is 0:
        _, _, save_result = roll(str(save_bonus))
    else:
        save_roll = show_advantage_roll(advantage)
        save_result = save_roll + save_bonus

    # Print result
    if save_result >= int(save_dc):
        print("SUCCESS: " + str(save_result))
    else:
        print("FAILURE: " + str(save_result))

if __name__ == "__main__":
    show_save(1, 13, advantage=0)
