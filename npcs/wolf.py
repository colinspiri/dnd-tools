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
        }, {})

    def action(self, action_name):
        if "bite" in action_name:
            self.action_bite()
        else:
            print("Action name not recognized.")
    def action_bite(self):
        to_hit = "+4"
        damage = "2d4+2"
        print(self.name + " attacks with " + to_hit + " to hit and " + damage + " piercing damage.")
        dice.show_attack(to_hit, damage)
        print("If the target is a creature, it must succeed on a DC 11 STR saving throw or be knocked prone.")
