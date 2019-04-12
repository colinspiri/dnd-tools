from creature import Creature
import constants
import dice
import jsonloader as loader

class NPC(Creature):
    def __init__(self, object):
        Creature.__init__(self, object["name"])
        rolls, modifier, result = dice.roll(object["max_health"])
        self.max_health = result
        self.current_health = self.max_health
        self.armor_class = object["armor_class"]

        # Ability scores
        self.ability_scores = object["ability_scores"]
        self.ability_modifiers = {}
        for ability, score in self.ability_scores.items():
            self.ability_modifiers[ability] = constants.ABILITY_MODIFIERS[score]

        # Saving throws
        self.saving_throws = self.ability_modifiers.copy()
        for ability, modifier in object["saving_throws"].items():
            self.saving_throws[ability] = modifier

        self.actions = object["actions"]

    def action(self, requested_action):
        for action_name, action in self.actions.items():
            if action_name == requested_action:
                # Show to hit and basic damage amount
                to_hit = action["to_hit"]
                basic_damage_dice = action["damage"][0]["damage_dice"]
                basic_damage_type = action["damage"][0]["damage_type"]
                to_hit_result, damage_result, critical = dice.show_attack(to_hit, basic_damage_dice, basic_damage_type)
                # If critical failure, don't show extra damage
                if critical == False:
                    return
                # If more damage in array, show bonus damage
                for i in range(1, len(action["damage"])):
                    damage_tuple = dice.roll(action["damage"][i]["damage_dice"])
                    damage_result = damage_tuple[2]
                    print("Bonus Damage: " + str(damage_result) + " (" + action["damage"][i]["damage_type"] + ")")
                # Show effects
                for i in range(len(action["effects"])):
                    print("-" + action["effects"][i])
                return

        print("Action name not recognized.")

    def save(self, ability, save_dc):
        save_bonus = self.saving_throws[ability]
        save_success, saving_throw = dice.show_save(str(save_bonus), save_dc)
        return save_success, saving_throw

    def __str__(self):
        return self.name + " has " + str(self.current_health) + "/" + str(self.max_health) + " health."

if __name__ == "__main__":
    npc = NPC(loader.get_creature("wolf"))
    print(npc)
    npc.action("bite")
