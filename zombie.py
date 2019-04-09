from npc import NPC
import dice

class Zombie(NPC):
    def __init__(self):
        rolls, modifier, result = dice.roll("3d8+9")
        NPC.__init__(self, "Zombie", result,
        {
        'STR': 13,
        'DEX': 6,
        'CON': 16,
        'INT': 3,
        'WIS': 6,
        'CHA': 5
        })

    def attack(self, attack_name):
        if attack_name == "slam":
            self.attack_slam()
        else:
            print("Attack name not recognized.")

    def attack_slam(self):
        to_hit_tuple = dice.roll("+3")
        to_hit = to_hit_tuple[2]
        print("To Hit: " + str(to_hit))
        damage_tuple = dice.roll("1d6+1")
        damage = damage_tuple[2]
        print("Damage: " + str(damage) + " (bludgeoning)")

    def __str__(self):
        return self.name + " has " + str(self.get_current_health()) + "/" + str(self.max_health) + " health."
