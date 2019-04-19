import initiative as init
import dice

def get_input(initiative):
    text_elements = input("> ").strip().split()
    if len(text_elements) == 0:
        print("Invalid input. Try again, but with words this time.")
    else:
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
            rolls, modifier, damage_amount = dice.show_roll(damage_amount)
        initiative.damage_current_creature(int(damage_amount))

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
        commands = ["help", "next", "end", "roll", "damage", "remove", "action", "save"]
        print("Here's a list of available commands: " + str(commands))

    else:
        print("Command not recognized. Type \'help\' for a list of available commands.")
