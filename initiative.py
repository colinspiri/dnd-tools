from entity import Entity
from npc import NPC
import jsonloader as loader
import dice


class Initiative:
    def __init__(self):
        self.order = []
        self.turn = 0
        self.round = 0

    def add_entity(self, entity, score):
        self.order.append({
            "entity": entity,
            "score": score
        })
        self.sort()

    def get_current_entity(self):
        return self.order[self.turn]["entity"]

    def get_entity(self, name):
        for set in self.order:
            entity = set["entity"]
            if name.lower() == entity.name.lower():
                return entity
            else:
                try:
                    for command in entity.commands:
                        if name.lower() == command.lower():
                            return entity
                except Exception:
                    pass

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
        def get_entity_score(entity):
            return entity["score"]
        self.order.sort(key=get_entity_score, reverse=True)

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
        print(entity.name + " (" + str(self.order[self.turn]["score"]) + ") is up.")
        if entity.damage_taken > 0:
            print(str(entity.damage_taken) + " damage taken.")
        try:
            print("Max HP: " + str(entity.max_hit_points))
        except Exception:
            pass

    def show_round(self):
        print("\n\n")
        print("ROUND " + str(self.round + 1) + ":")

    def show_order(self):
        print()
        print("Initiative Order: ")
        for element in self.order:
            print(element["entity"].name + " (" + str(element["score"]) + ")")

    def end_initiative(self):
        pcs_to_update = []
        for set in self.order:
            if hasattr(set["entity"], "json_object"):
                pcs_to_update.append(set["entity"])
        if len(pcs_to_update) > 0:
            text = input("Save player character data? ").strip()
            if text == "yes" or text == "y":
                loader.update_pcs(pcs_to_update)
        print("Program ended.")
        quit()


def input_initiative():
    print("Enter initiative in form \"<count> name <initiative score>\".")
    init = Initiative()
    while True:
        # Get input as list of words
        text = input("> ").strip()
        if text == "":
            break
        words = text.split()
        # Initialize parameters to pass to add_to_initiative()
        count = 1
        name_index = 0
        if words[0].isdigit():
            name_index = 1
            count = int(words[0])
        name = words[name_index].lower()
        try:
            score = int(words[name_index + 1])
        except Exception:
            score = False
        add_to_initiative(init, count, name, score)
    return init


def add_to_initiative(init, count, name, score):
    # Add a number of entities equal to count
    for i in range(count):
        # Use JSON stats if found, otherwise just make blank Entity
        try:
            entity = NPC(loader.get_npc(name))
            print("Loaded " + entity.name + " stats.")
            # Append numbers to all commands if multiple
            if count > 1:
                for c in range(len(entity.commands)):
                    entity.commands[c] += str(i + 1)
        except Exception:
            entity = Entity(name.capitalize())

        # Append numbers to name if multiple
        if count > 1:
            entity.name += str(i + 1)

        # Roll for initiative if none given
        if score is False:
            init_score = dice.random_int(20)
            # Add DEX if the entity has it
            try:
                init_score += entity.ability_modifiers["DEX"]
            except Exception:
                pass
            print("Rolled " + str(init_score) + " for initiative.")
        else:
            init_score = score
        init.add_entity(entity, init_score)
