from creature import Creature
import constants
import dice

class NPC(Creature):
    def __init__(self, name, max_health, ability_scores, saving_throw_proficiencies):
        Creature.__init__(self, name)
        self.max_health = max_health
        self.current_health = self.max_health

        # Ability scores
        self.ability_scores = ability_scores
        self.ability_modifiers = {}
        for ability, score in self.ability_scores.items():
            self.ability_modifiers[ability] = constants.ABILITY_MODIFIERS[score]

        # Saving throws
        self.saving_throws = self.ability_modifiers.copy()
        for ability, modifier in saving_throw_proficiencies.items():
            self.saving_throws[ability] = modifier

    def save(self, ability, save_dc):
        save_bonus = self.saving_throws[ability]
        save_success, saving_throw = dice.show_save(str(save_bonus), save_dc)
        return save_success, saving_throw

    def __str__(self):
        return self.name + " has " + str(self.current_health) + "/" + str(self.max_health) + " health."

if __name__ == "__main__":
    npc = NPC("bob", 20, {
    'STR': 13,
    'DEX': 6,
    'CON': 16,
    'INT': 3,
    'WIS': 6,
    'CHA': 5
    }, {
    'WIS': 0
    })
    print(npc.saving_throws)
