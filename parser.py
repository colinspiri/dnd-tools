import initiative as init
import dice
import jsonloader as loader

def get_input(initiative):
    text = input("> ").strip()
    if len(text) == 0:
        print("Invalid input. Try again, but with words this time.")
    else:
        process_input(initiative, text)

def process_input(initiative, text):
    text_elements = text.strip().split()
    command = text_elements[0]
    text_elements.remove(command)
    run_command(initiative, command, text_elements)

def run_command(initiative, command, components):
    # Next
    if command == "next":
        initiative.next_turn()

    # End
    elif command == "end":
        print("Program ended.")
        quit()

    # Roll
    elif command == "roll":
        if len(components) == 0:
            print("Invalid input. Roll command requires more components.")
            return
        # Roll attack
        elif components[0] == "attack":
            dice.show_attack(components[1], components[2])
        # Roll save
        elif components[0] == "save":
            dice.show_save(components[1], components[2])
        # Roll DICE
        else:
            dice.show_roll("".join(components))

    # Damage
    elif command == "damage":
        if len(components) == 0:
            print("Invalid input. Damage command requires more components.")
            return
        damage_amount = "".join(components)
        if not damage_amount.isdigit():
            _, _, damage_amount = dice.show_roll(damage_amount)
        initiative.damage_current_creature(int(damage_amount))

    # Heal
    elif command == "heal":
        if len(components) == 0:
            print("Invalid input. Heal command requires a parameter.")
            return
        heal_amount = "".join(components)
        if not heal_amount.isdigit():
            _, _, heal_amount = dice.show_roll(heal_amount)
        initiative.damage_current_creature(-1*int(heal_amount))

    # Remove
    elif command == "remove":
        if len(components) == 0:
            initiative.get_current_creature().dead = True
        # Remove INDEX
        else:
            initiative.order[int(components[0])]["creature"].dead = True
        initiative.remove_dead_creatures()

    # Action
    elif command == "action":
        creature = initiative.get_current_creature()
        if len(components) == 0:
            creature.show_actions()
        # Action ACTION_NAME
        else:
            creature.action(components[0])

    # Save
    elif command == "save":
        if len(components) == 0:
            print("Invalid input. Save command requires more components.")
            return
        creature = initiative.get_current_creature()
        # Save ABILITY DC
        try:
            ability = components[0].upper()
            save_dc = components[1]
            print(ability, save_dc)
            creature.save(ability, save_dc)
        except:
            print(creature.name + " has no saving throw stats to use.")

    # Help
    elif command == "help":
        if len(components) == 0:
            commands = loader.get_command_names()
            print("Here's a list of available commands: " + str(commands))
        else:
            print(loader.get_command_description(components[0]))

    # Command not recognized.
    else:
        print("Command not recognized. Type \'help\' for a list of available commands.")
