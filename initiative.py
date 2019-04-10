from creature import Creature
from npcs.wolf import Wolf
from npcs.zombie import Zombie
from npcs.werewolf import Werewolf
from npcs.druid import Druid
from npcs.vampirespawn import VampireSpawn
from npcs.nighthag import NightHag
from npcs.strahd import Strahd

def input_initiative():
    creature_order = []

    # Store input into order of creatures
    print("Enter initiative in form \"NAME INITIATIVE\".")
    while True:
        text = input("> ").strip()
        if text == "":
            break
        words = text.split()
        name = words[0].lower()
        if name == "wolf":
            new_creature = Wolf()
        elif name == "zombie":
            new_creature = Zombie()
        elif name == "werewolf":
            new_creature = Werewolf()
        elif name == "druid":
            new_creature = Druid()
        elif name == "vampirespawn":
            new_creature = VampireSpawn()
        elif name == "nighthag":
            new_creature = NightHag()
        elif name == "strahd":
            new_creature = Strahd()
        else:
            new_creature = Creature(name.capitalize())
        new_creature.set_initiative(int(words[1]))
        creature_order.append(new_creature)

    # Sort creature order by initiative count
    def get_creature_initiative(creature):
        return creature.initiative
    creature_order.sort(key = get_creature_initiative, reverse = True)
    return creature_order

def show_initiative(creature_order):
    print()
    print("Initiative Order: ")
    for creature in creature_order:
        print(creature.name + " (" + str(creature.initiative) + ")")

def next_round(turn, rounds):
    turn = 0
    rounds += 1
    print("\n\n\n")
    print("ROUND " + str(rounds) + ":")
    return turn, rounds


if __name__ == "__main__":
    order = input_initiative()
    show_initiative(order)

    # Cycle through order
    rounds = 0
    turn = 0
    print("ROUND 1:")
    while True:
        print(order[turn].name + " (" + str(order[turn].initiative) + ") is up." )
        text = input("Next? ").strip()
        turn += 1
        if turn >= len(order):
            turn = 0
            rounds += 1
            print()
            print("ROUND " + str(rounds + 1) + ":")
