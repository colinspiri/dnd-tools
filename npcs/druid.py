from npc import NPC
import dice

class Druid(NPC):
    def __init__(self):
        rolls, modifier, result = dice.roll("5d8+5")
        NPC.__init__(self, "Druid", result,
        {
        'STR': 10,
        'DEX': 12,
        'CON': 13,
        'INT': 12,
        'WIS': 15,
        'CHA': 11
        }, {})

    def action(self, action_name):
        if "staff" in action_name:
            self.action_quarterstaff()
        else:
            print("Action name not recognized.")
    def action_quarterstaff(self):
        to_hit = "+2"
        damage = "1d6"
        print(self.name + " attacks with " + to_hit + " to hit for " + damage + " bludgeoning damage.")
        dice.show_attack(to_hit, damage)
