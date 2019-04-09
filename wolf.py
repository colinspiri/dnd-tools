from npc import NPC
import dice

class Wolf(NPC):
    def __init__(self):
        rolls, modifier, result = dice.roll("2d8+2")
        NPC.__init__(self, "Wolf", result,
        {
        'STR': 12,
        'DEX': 15,
        'CON': 12,
        'INT': 3,
        'WIS': 12,
        'CHA': 6
        })

    def attack(self, attack_name):
        if attack_name == "bite":
            self.attack_bite()
        else:
            print("Attack name not recognized.")

    def attack_bite(self):
        to_hit_tuple = dice.roll("+4")
        to_hit = to_hit_tuple[2]
        print("To Hit: " + str(to_hit))
        damage_tuple = dice.roll("2d4+2")
        damage = damage_tuple[2]
        print("Damage: " + str(damage) + " (piercing)")
        print("If the target is a creature, it must succeed on a DC 11 STR saving throw or be knocked prone.")

    def __str__(self):
        return "Wolf has " + str(self.get_current_health()) + "/" + str(self.max_health) + " health."

if __name__ == "__main__":
    wolf = Wolf()
    print(str(wolf))
