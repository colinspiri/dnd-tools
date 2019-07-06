from creature import Creature
import constants
import dice
import jsonloader as loader

class NPC(Creature):
    def __init__(self, object):
        _, _, max_health = dice.roll(object["max_health"])
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

        Creature.__init__(self, object["name"], max_health, object["actions"])

    

    def save(self, ability, save_dc):
        save_bonus = self.saving_throws[ability]
        save_success, saving_throw = dice.show_save(str(save_bonus), save_dc)
        return save_success, saving_throw

if __name__ == "__main__":
    npc = NPC(loader.get_creature("strahd"))
    print(npc.saving_throws)
    npc.action("bite")
