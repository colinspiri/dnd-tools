# import initiative as init
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
    if command == "next" or command == "n":
        initiative.next_turn()
    elif command == "e" or command == "end" or command == "q" or command == "quit":
        initiative.end_initiative()
    elif command == "r" or command == "roll":
        command_roll(components)
    elif command == "d" or command == "damage":
        command_damage(initiative, components)
    elif command == "h" or command == "heal":
        command_heal(initiative, components)
    elif command == "rm" or command == "rem" or command == "remove":
        command_remove(initiative, components)
    elif command == "a" or command == "action":
        command_action(initiative, components)
    elif command == "save":
        command_save(initiative, components)
    elif command == "check":
        command_check(initiative, components)
    elif command == "rest":
        command_rest(initiative, components)
    elif command == "help":
        command_help(components)
    else:
        print("Command not recognized. Available commands:")
        command_help([])


def command_roll(components):
    if len(components) == 0:
        dice.show_roll("d20", advantage=0)
        return
    # Parse for advantage
    advantage = 0
    last_component = components[len(components)-1]
    if last_component == "a" or last_component == "adv" or last_component == "advantage":
        advantage = 1
    elif last_component == "d" or last_component == "dis" or last_component == "disadvantage":
        advantage = -1
    # Roll attack
    if components[0] == "attack":
        dice.show_attack(int(components[1]), components[2], advantage=advantage)
    # Roll save
    elif components[0] == "save":
        dice.show_save(int(components[1]), components[2], advantage=advantage)
    # Roll standard dice
    else:
        dice.show_roll(components[0], advantage=advantage)


def command_damage(initiative, components, heal=False):
    if len(components) == 0:
        print("Invalid input. Damage command requires more parameters.")
        return
    elif len(components) == 1:
        entity = initiative.get_current_entity()
        amount = components[0]
    else:
        entity = initiative.get_entity(components[0])
        amount = components[1]
    if not amount.isdigit():
        _, _, amount = dice.show_roll(amount)
    initiative.damage_entity(entity, -int(amount) if heal else int(amount))
    print(entity)


def command_heal(initiative, components):
    command_damage(initiative, components, True)


def command_remove(initiative, components):
    if len(components) == 0:
        initiative.get_current_entity().dead = True
    # Remove by index
    else:
        initiative.order[int(components[0])]["creature"].dead = True
    initiative.remove_dead_entities()


def command_action(initiative, components):
    entity = initiative.get_current_entity()
    if len(components) == 0:
        entity.show_actions()
    # Action ACTION_NAME
    else:
        entity.action(components[0])


def command_save(initiative, components):
    if len(components) == 0:
        print("Invalid input. Save command requires more parameters.")
        return
    entity = initiative.get_current_entity()
    save_dc = None
    advantage = 0
    if len(components) == 3:
        if components[2] == "adv" or components[2] == "advantage":
            advantage = 1
        elif components[2] == "dis" or components[2] == "disadvantage":
            advantage = -1
    if not hasattr(entity, "saving_throws"):
        print(entity.name + " cannot roll a saving throw. Did you want a d20 roll?")
        dice.show_roll("d20", advantage)
        return
    if len(components) >= 2:
        save_dc = components[1]
    ability = components[0].upper()
    try:
        entity.make_save(ability, save_dc, advantage=advantage)
    except Exception:
        if save_dc is None:
            print(entity.name + " has no saving throw named \'" + ability + "\'.")
        else:
            print("\'" + ability + "\' and \'" + save_dc + "\' not recognized as valid input for ABILITY and SAVE DC.")


def command_check(initiative, components):
    if len(components) == 0:
        print("Invalid input. Check command requires more parameters.")
        return
    entity = initiative.get_current_entity()
    # Get advantage
    advantage = 0
    last_component = components.pop(len(components) - 1)
    if last_component == "adv":
        advantage = 1
    elif last_component == "dis":
        advantage = -1
    else:
        components.append(last_component)
    # Get skill
    if not hasattr(entity, "skills"):
        print(entity.name + " cannot roll a skill check. Did you want a d20 roll?")
        dice.show_roll("d20", advantage)
        return
    skill = "_".join(components).lower()
    try:
        entity.skill_check(skill, advantage)
    except Exception:
        print(entity.name + " has no skill or ability named \'" + skill + "\'.")


def command_rest(initiative, components):
    if len(components) == 0:
        print("Invalid input. Rest command requires more parameters.")
        return
    entity = initiative.get_current_entity()
    if not hasattr(entity, "current_hit_dice"):
        print(entity.name + " cannot take a rest.")
        return
    # Short rest
    if components[0] == "short":
        print("Short resting...")
        entity.take_short_rest()
    # Long rest
    elif components[0] == "long":
        print("Long resting...")
        entity.take_long_rest()
    else:
        print("\'" + components[0] + "\' not recognized as a valid rest type. Choose either \'short\' or \'long\'.")


def command_help(components):
    if len(components) == 0:
        commands = loader.get_command_names()
        print("Here's a list of available commands: " + str(commands))
    else:
        print(loader.get_command_description(components[0]))
