from creature import Creature
import constants
import dice
import jsonloader as loader

class PC(Creature):
    def __init__(self, object):
        Creature.__init__(self, object["max_health"], {}, object)
        self.json_object = object

        self.current_health = object["current_health"]

        # Skill proficiencies
        self.proficiency_bonus = object["proficiency_bonus"]
        self.skills = {}
        for skill, ability in constants.SKILLS.items():
            self.skills[skill] = self.ability_modifiers[ability]
        for skill, proficiency in object["skill_proficiencies"].items():
            self.skills[skill] += proficiency * self.proficiency_bonus

        # Compiling actions from weapon proficiencies and weapon properties
        self.weapon_proficiencies = object["weapon_proficiencies"]
        self.weapons = object["weapons"]
        actions = {}
        for weapon in self.weapons:
            weapon_stats = loader.get_weapon(weapon)
            # Relevant ability bonus
            if "finesse" in weapon_stats["properties"]:
                if self.ability_modifiers["STR"] >= self.ability_modifiers["DEX"]:
                    relevant_ability = "STR"
                else:
                    relevant_ability = "DEX"
            elif weapon_stats["range"] == "melee":
                relevant_ability = "STR"
            else:
                relevant_ability = "DEX"
            relevant_ability_bonus = self.ability_modifiers[relevant_ability]
            # To hit modifier
            to_hit = relevant_ability_bonus
            if weapon in self.weapon_proficiencies or weapon_stats["type"] in self.weapon_proficiencies:
                to_hit += self.proficiency_bonus
            if to_hit > 0:
                to_hit = "+" + str(to_hit)
            else:
                to_hit = str(to_hit)
            # Damage
            damage = weapon_stats["damage_dice"]
            if damage != "0" and relevant_ability_bonus > 0:
                damage += "+" + str(relevant_ability_bonus)
            elif relevant_ability_bonus < 0:
                damage += str(relevant_ability_bonus)
            # Convert to action dictionary
            action_name = weapon
            try:
                formatted_name = weapon_stats["name"]
            except:
                formatted_name = weapon.capitalize()
            versatile = False
            if "versatile" in weapon_stats["properties"]:
                action_name += " 1"
                formatted_name += ", One-Handed"
                versatile = True
            range = weapon_stats["range"]
            if "reach" in weapon_stats["properties"]:
                range += " + 5ft"
            actions[action_name] = loader.get_simple_action_dictionary(formatted_name, range, to_hit, damage, weapon_stats["damage_type"])
            if "special" in weapon_stats["properties"]:
                actions[action_name]["effects"] = weapon_stats["effects"]
            # Add commands
            try:
                if versatile:
                    actions[action_name]["commands"] = []
                    for command in weapon_stats["commands"]:
                        actions[action_name]["commands"].append(command + " 1")
                else:
                    actions[action_name]["commands"] = weapon_stats["commands"]
            except:
                pass
            # If versatile, add another action with alt damage dice and different commands
            if versatile:
                action_name = weapon + " 2"
                try:
                    formatted_name = weapon_stats["name"] + ", Two-Handed"
                except:
                    formatted_name = weapon.capitalize() + ", Two-Handed"
                alternate_damage = weapon_stats["alternate_damage_dice"]
                if relevant_ability_bonus > 0:
                    alternate_damage += "+" + str(relevant_ability_bonus)
                elif relevant_ability_bonus < 0:
                    alternate_damage += str(relevant_ability_bonus)
                actions[action_name] = loader.get_simple_action_dictionary(formatted_name, range, to_hit, alternate_damage, weapon_stats["damage_type"])
                try:
                    actions[action_name]["commands"] = []
                    for command in weapon_stats["commands"]:
                        actions[action_name]["commands"].append(command + " 2")
                except:
                    pass
            if "thrown" in weapon_stats["properties"]:
                action_name = weapon + " thrown"
                formatted_name += ", Thrown"
                actions[action_name] = loader.get_simple_action_dictionary(formatted_name, weapon_stats["thrown_range"], to_hit, damage, weapon_stats["damage_type"])
        self.set_actions(actions)

    def take_damage(self, damage):
        self.damage_taken += damage
        self.current_health -= damage
        if self.current_health <= -self.max_health:
            print(self.name + " has dropped to " + str(self.current_health) + "/" + str(self.max_health) + " hit points, and is now dead.")
        elif self.current_health <= 0:
            self.current_health = 0
            print(self.name + " has dropped to 0 hit points and is now unconscious. " + self.name + " will now make death saving throws.")
        else:
            if self.current_health > self.max_health:
                self.current_health = self.max_health
                self.damage_taken = 0
            print(self.name + " has " + str(self.current_health) + "/" + str(self.max_health) + " hit points.")
        self.json_object["current_health"] = self.current_health

    def skill_check(self, skill):
        skill_bonus = self.skills[skill]
        dice.show_roll(str(skill_bonus))

    def str_ability_scores(self):
        text = "Ability Scores: \n"
        for ability, score in self.ability_scores.items():
            modifier = self.ability_modifiers[ability]
            if modifier > 0:
                text += ability + ": " + str(score) + " (+" + str(modifier) + ")\n"
            else:
                text += ability + ": " + str(score) + " (" + str(modifier) + ")\n"
        return text
    def str_weapons(self):
        text = "Weapons: "
        for i in range(len(self.weapons)):
            text += self.weapons[i]
            if i < len(self.weapons) - 1:
                text += ", "
        text += "\n"
        return text

    def __str__(self):
        text = self.name + "\n"
        text += "HP: " + str(self.current_health) + "/" + str(self.max_health) + "\n"
        text += "AC: " + str(self.armor_class) + "\n"
        text += self.str_ability_scores()
        text += self.str_weapons()
        text += self.str_actions()

        return text + "\n"

if __name__ == "__main__":
    pc = PC(loader.get_pc("igor"))
    print(pc)
    pc.action("dagger thrown")
