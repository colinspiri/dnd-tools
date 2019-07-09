from entity import Entity
import constants
import dice

class Creature(Entity):
    def __init__(self, max_hit_points, actions, json_object):
        Entity.__init__(self, json_object["name"])
        try:
            commands = json_object["commands"]
        except:
            commands = []
        self.commands = commands

        self.max_hit_points = max_hit_points
        self.armor_class = json_object["armor_class"]

        # Ability scores
        self.ability_scores = json_object["ability_scores"]
        self.ability_modifiers = {}
        for ability, score in self.ability_scores.items():
            self.ability_modifiers[ability] = constants.ABILITY_MODIFIERS[score]

        # Saving throws
        self.saving_throws = self.ability_modifiers.copy()
        for ability, modifier in json_object["saving_throws"].items():
            self.saving_throws[ability] = modifier

        self.actions = actions

    def save(self, ability, save_dc):
        save_bonus = self.saving_throws[ability]
        if save_dc is not None:
            save_success, save_result = dice.show_save(str(save_bonus), save_dc)
            return save_success, save_result
        else:
            _, _, save_result = dice.show_roll(str(save_bonus))
            return None, save_result

    def set_actions(self, actions):
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
        return self.name + " has " + str(self.current_hit_points) + "/" + str(self.max_hit_points) + " hit points."
