from entity import Entity
import constants
import dice

class Creature(Entity):
    def __init__(self, name, max_health, actions):
        Entity.__init__(self, name)
        self.max_health = max_health
        self.current_health = self.max_health

        self.actions = actions

    def show_actions(self):
        print(self.name + " has actions " + str(list(self.actions.keys())))
    def action(self, requested_action):
        for action_name, action in self.actions.items():
            # Check actual action name
            if action_name == requested_action:
                self.execute_action(action)
                return
            # Check commands also
            try:
                for command in action["commands"]:
                    if command == requested_action:
                        self.execute_action(action)
                        return
            except:
                pass
        print("Action name not recognized.")
    def execute_action(self, action):
        # Get to hit and damage amounts
        to_hit = action["to_hit"]
        damages = action["damage"]
        basic_damage_dice = damages[0]["damage_dice"]
        basic_damage_type = damages[0]["damage_type"]

        # Show summary of action
        summary = self.name + " attacks at a range of " + action["range"] + " with " + to_hit + " to hit and deals " + basic_damage_dice + " " + basic_damage_type + " damage"
        for i in range(1, len(damages)):
            summary += " and " + damages[i]["damage_dice"] + " " + damages[i]["damage_type"] + " damage"
        summary += "."
        print(summary)

        # Show attack with basic damage
        critical = dice.show_attack(to_hit, basic_damage_dice, basic_damage_type)[2]

        # If critical failure, don't show extra damage
        if critical == False:
            return
        # If more damage in array, show bonus damage
        for i in range(1, len(damages)):
            damage_tuple = dice.roll(damages[i]["damage_dice"])
            damage_result = damage_tuple[2]
            print("Bonus Damage: " + str(damage_result) + " (" + damages[i]["damage_type"] + ")")
        # Show effects
        for i in range(len(action["effects"])):
            print("-" + action["effects"][i])
        return

    def str_actions(self):
        text = "Actions: \n"
        for action_name in self.actions.keys():
            text += self.str_action_long(action_name)
        text += "\n"
        return text
    def str_action_long(self, action_name):
        action = self.actions[action_name]
        text = action["name"] + ". "
        if action["range"] == "melee":
            text += "Melee weapon attack: "
        else:
            text += "Ranged weapon attack: "
        text += action["to_hit"] + " to hit, reach " + action["range"] + ", one target. "
        damages = action["damage"]
        text += "Hit: (" + damages[0]["damage_dice"] + ") " + damages[0]["damage_type"] + " damage"
        for i in range(1, len(damages)):
            text += " and (" + damages[i]["damage_dice"] + ") " + damages[i]["damage_type"] + " damage"
        text += ".\n"
        return text
    def str_action_short(self, action_name):
        action = self.actions[action_name]
        damages = action["damage"]
        text = action_name + ": " + action["to_hit"] + ", (" + damages[0]["damage_dice"] + ") " + damages[0]["damage_type"] + " damage"
        for i in range(1, len(damages)):
            text += " + (" + damages[i]["damage_dice"] + ") " + damages[i]["damage_type"] + " damage"
        text += "\n"
        return text
    def __str__(self):
        return self.name + " has " + str(self.current_health) + "/" + str(self.max_health) + " health."
