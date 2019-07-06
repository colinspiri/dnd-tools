from entity import Entity
from npc import NPC
import jsonloader as loader
import dice

class Initiative:
    def __init__(self):
        self.order = []
        self.turn = 0
        self.round = 0

    def add_entity(self, entity, initiative):
        self.order.append({
        "entity": entity,
        "initiative": initiative
        })
        self.sort()
    def get_current_entity(self):
        return self.order[self.turn]["entity"]
    def get_entity(self, name):
        for set in self.order:
            if set["entity"].name.lower() == name.lower():
                return set["entity"]

    def damage_current_entity(self, damage_amount):
        self.damage_entity(self.get_current_entity(), damage_amount)

    def damage_entity(self, entity, damage_amount):
        # Take damage
        entity.take_damage(damage_amount)
        # If dead, remove from order and adjust accordingly
        if entity.dead:
            self.remove_dead_entities()

    def remove_dead_entities(self):
        # Copy all elements into new order
        new_order = []
        for i in range(len(self.order)):
            element = self.order[i]
            entity = element["entity"]
            if not entity.dead:
                new_order.append(element)
            elif i < self.turn:
                self.turn -= 1
        self.order = new_order

        # Special cases
        if len(self.order) == 0:
            print("No entities left in initiative. Program ended.")
            quit()
        if self.turn == len(self.order):
            self.next_round()

    def sort(self):
        def get_entity_initiative(entity):
            return entity["initiative"]
        self.order.sort(key = get_entity_initiative, reverse = True)

    def next_turn(self):
        self.turn += 1
        if self.turn >= len(self.order):
            self.next_round()
    def next_round(self):
        self.turn = 0
        self.round += 1
        self.show_round()

    def show_turn(self):
        entity = self.get_current_entity()
        print(entity.name + " (" + str(self.order[self.turn]["initiative"]) + ") is up." )
        if entity.damage_taken > 0:
            print(str(entity.damage_taken) + " damage taken.")
        try:
            print("Health: " + str(entity.current_health) + "/" + str(entity.max_health))
        except:
            pass
    def show_round(self):
        print("\n\n")
        print("ROUND " + str(self.round + 1) + ":")
    def show_order(self):
        print()
        print("Initiative Order: ")
        for element in self.order:
            print(element["entity"].name + " (" + str(element["initiative"]) + ")")


def input_initiative():
    initiative = Initiative()
    print("Enter initiative in form \"[Count] Name [Initiative]\".")
    while True:
        # Get input
        text = input("> ").strip()
        if text == "":
            break
        words = text.split()
        if words[0].isdigit():
            count_specified = True
            entity_count = int(words[0])
            name = words[1].lower()
        else:
            count_specified = False
            name = words[0].lower()
            entity_count = 1

        # If creature name is found in JSON, use it; otherwise, make an Entity object
        try:
            new_entity = NPC(loader.get_creature(name))
        except:
            new_entity = Entity(name.capitalize())

        # Get the initiative roll
        try:
            if count_specified:
                initiative_result = int(words[2])
            else:
                initiative_result = int(words[1])
        except:
            initiative_result = dice.random_int(20)
            try:
                initiative_result += new_entity.ability_modifiers["DEX"]
            except:
                pass
            print("Rolled " + str(initiative_result) + " for initiative.")

        # Add it to the order
        if words[0].isdigit():
            for i in range(entity_count):
                try:
                    new_entity_instance = NPC(loader.get_creature(name))
                except:
                    new_entity_instance = Entity(name.capitalize())
                new_entity_instance.name = new_entity_instance.name + str(i + 1)
                initiative.add_entity(new_entity_instance, initiative_result)
        else:
            initiative.add_entity(new_entity, initiative_result)
    return initiative
