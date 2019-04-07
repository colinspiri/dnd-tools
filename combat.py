import initiative as init
import dice

# Get initiative order
order = init.input_initiative()
init.show_initiative(order)

# Cycle through order
current_turn = 0
while True:
    print(order[current_turn]["name"] + " (" + str(order[current_turn]["initiative"]) + ") is up." )

    text = input("> ").strip()
    command_roll = "roll"
    command_next = "n"
    if (command_roll + " ") in text:
        dice.roll_from_input(text[text.find(command_roll + " ") + len(command_roll + " "):])
    # elif "take " in text:
        # take direct numbers as damage and add as element in order objects
        # also be able to take dice amounts of damage
        # eventually add monster classes with pre-determined attack rolls to call like "attack crossbow" or "attack claws" that roll to hit and for damage
    elif command_next in text:
        current_turn += 1
        current_turn %= len(order)
