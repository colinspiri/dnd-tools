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

    def action(self, action_name):
        if "slam" in action_name:
            self.action_slam()
        else:
            print("Action name not recognized.")

    def action_slam(self):
        to_hit = "+3"
        damage = "1d6+1"
        print(self.name + " attacks with " + to_hit + " to hit and " + damage + " bludgeoning damage.")
        dice.show_attack(to_hit, damage)
