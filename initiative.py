from entity import Entity
from npc import NPC
import jsonloader as loader

class Initiative:
    def __init__(self):
        self.order = []
        self.turn = 0
        self.round = 0

    def add_creature(self, creature, initiative):
        self.order.append({
        "creature": creature,
        "initiative": initiative
        })
        self.sort()
    def get_current_creature(self):
        return self.order[self.turn]["creature"]

    def damage_current_creature(self, damage_amount):
        # Take damage
        creature = self.get_current_creature()
        creature.take_damage(damage_amount)
        # If dead, remove from order and adjust accordingly
        if creature.dead:
            self.remove_dead_creatures()

    def remove_dead_creatures(self):
        # Copy all elements into new order
        new_order = []
        for i in range(len(self.order)):
            element = self.order[i]
            creature = element["creature"]
            if not creature.dead:
                new_order.append(element)
            elif i < self.turn:
                self.turn -= 1
        self.order = new_order

        # Special cases
        if len(self.order) == 0:
            print("No creatures left in initiative. Program ended.")
            quit()
        if self.turn == len(self.order):
            self.next_round()

    def sort(self):
        def get_creature_initiative(creature):
            return creature["initiative"]
        self.order.sort(key = get_creature_initiative, reverse = True)

    def next_turn(self):
        self.turn += 1
        if self.turn >= len(self.order):
            self.next_round()
    def next_round(self):
        self.turn = 0
        self.round += 1
        self.show_round()

    def show_turn(self):
        creature = self.get_current_creature()
        print(creature.name + " (" + str(self.order[self.turn]["initiative"]) + ") is up." )
        if creature.damage_taken > 0:
            print(str(creature.damage_taken) + " damage taken.")
        try:
            print("Health: " + str(creature.current_health) + "/" + str(creature.max_health))
        except:
            pass
    def show_round(self):
        print("\n\n")
        print("ROUND " + str(self.round + 1) + ":")
    def show_order(self):
        print()
        print("Initiative Order: ")
        for element in self.order:
            print(element["creature"].name + " (" + str(element["initiative"]) + ")")


def input_initiative():
    initiative = Initiative()

    # Store input into order of creatures
    print("Enter initiative in form \"NAME INITIATIVE\".")
    while True:
        text = input("> ").strip()
        if text == "":
            break
        words = text.split()
        name = words[0].lower()
        # If name is found in JSON file, use it; otherwise, make a Creature object
        try:
            new_creature = NPC(loader.get_creature(name))
        except:
            new_creature = Entity(name.capitalize())
        initiative.add_creature(new_creature, int(words[1]))

    return initiative
