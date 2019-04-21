from creature import Creature
import constants
import dice
import jsonloader as loader

class PC(Creature):
    def __init__(self, object):
        self.armor_class = object["armor_class"]

        # Ability scores
        self.ability_scores = object["ability_scores"]
        self.ability_modifiers = {}
        for ability, score in self.ability_scores.items():
            self.ability_modifiers[ability] = constants.ABILITY_MODIFIERS[score]
        self.initiative_bonus = self.ability_modifiers["DEX"]

        # Saving throws
        self.saving_throws = self.ability_modifiers.copy()
        for ability, modifier in object["saving_throws"].items():
            self.saving_throws[ability] = modifier

        # Skill proficiencies
        self.proficiency_bonus = object["proficiency_bonus"]
        self.skills = {}
        for skill, ability in constants.SKILLS.items():
            self.skills[skill] = self.ability_modifiers[ability]
        for skill, proficiency in object["skill_proficiencies"].items():
            self.skills[skill] += proficiency * self.proficiency_bonus
        self.passive_perception = 10 + self.skills["perception"]

        # Weapon proficiencies and actions
        self.weapon_proficiencies = object["weapon_proficiencies"]
        self.weapons = object["weapons"]
        actions = {}
        for weapon in self.weapons:
            weapon_stats = loader.get_weapon(weapon)
            # To hit
            relevant_ability_bonus = self.ability_modifiers[weapon_stats["ability"]]
            to_hit = relevant_ability_bonus
            if weapon in self.weapon_proficiencies:
                to_hit += self.proficiency_bonus
            if to_hit > 0:
                to_hit = "+" + str(to_hit)
            else:
                to_hit = str("to_hit")
            # Damage
            damage = weapon_stats["damage_dice"]
            if relevant_ability_bonus > 0:
                damage += "+" + str(relevant_ability_bonus)
            elif relevant_ability_bonus < 0:
                damage += str(relevant_ability_bonus)
            # Convert to action dictionary
            actions[weapon] = {
            "to_hit": str(to_hit),
            "damage": [
            {
            "damage_dice": damage,
            "damage_type": weapon_stats["damage_type"]
            }
            ],
            "effects": []
            }
            try:
                actions[weapon]["commands"] = weapon_stats["commands"]
            except:
                pass
        Creature.__init__(self, object["name"], object["max_health"], actions)

    def save(self, ability, save_dc):
        save_bonus = self.saving_throws[ability]
        save_success, saving_throw = dice.show_save(str(save_bonus), save_dc)
        return save_success, saving_throw

if __name__ == "__main__":
    pc = PC(loader.get_pc("cha_racter"))
    print(pc)
    pc.action("longbow")
