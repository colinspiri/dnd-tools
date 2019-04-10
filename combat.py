import initiative as init
import dice

# Get initiative order
order = init.input_initiative()
init.show_initiative(order)

# Cycle through order
rounds = 1
turn = 0
print("ROUND 1:")
while True:
    if turn > 0:
        print()

    # Remove dead creatures
    if order[turn].dead:
        print(order[turn].name + " died and was removed from initiative.")
        del order[turn]
        if len(order) == 0:
            print("No creatures left in initiative. Program ended.")
            break
        if turn == len(order):
            turn, rounds = init.next_round(turn, rounds)
            continue

    # Print info about current creature
    print(order[turn].name + " (" + str(order[turn].initiative) + ") is up." )
    if hasattr(order[turn], 'max_health'):
        print("Health: " + str(order[turn].current_health) + "/" + str(order[turn].max_health))
    elif order[turn].damage_taken > 0:
        print(str(order[turn].damage_taken) + " damage taken.")

    # Input commands
    text = input("> ").strip()
    command_roll = "roll"
    command_roll_attack = "attack"
    command_damage = "damage"
    command_next = "next"
    command_remove = "remove"
    command_end = "end"
    command_action = "action"

    # Resolve commands
    if (command_roll + " ") in text:
        next_part = text[text.find(command_roll + " ") + len(command_roll + " "):]
        if command_roll_attack in next_part:
            elements = next_part.split()
            elements.remove(command_roll_attack)
            dice.show_attack(elements[0], elements[1])
        else:
            dice.show_roll(next_part)
        continue
    elif (command_damage + " ") in text:
        damage_amount = text[text.find(command_damage + " ") + len(command_damage + " "):]
        if not damage_amount.isdigit():
            rolls, modifier, damage_amount = dice.show_roll(damage_amount)
        order[turn].take_damage(int(damage_amount))
        continue
    elif text == command_remove:
        order[turn].dead = True
        continue
    elif text == command_next:
        turn += 1
        if turn >= len(order):
            turn, rounds = init.next_round(turn, rounds)
            continue
    elif text == command_end:
        print("Program ended.")
        break
    elif (command_action + " ") in text:
        if callable(getattr(order[turn], "action", None)):
            action_name = text[text.find(command_action + " ") + len(command_action + " "):]
            order[turn].action(action_name)
        else:
            print(order[turn].name + " has no actions.")
        continue
