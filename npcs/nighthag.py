from npc import NPC
import dice

class NightHag(NPC):
    def __init__(self):
        rolls, modifier, result = dice.roll("15d8+45")
        NPC.__init__(self, "Night Hag", result,
        {
        'STR': 18,
        'DEX': 15,
        'CON': 16,
        'INT': 16,
        'WIS': 14,
        'CHA': 16
        }, {})

    def action(self, action_name):
        if "claw" in action_name:
            self.action_claw()
        else:
            print("Action name not recognized.")
    def action_claw(self):
        to_hit = "+7"
        damage = "2d8+4"
        print(self.name + " attacks with " + to_hit + " to hit for " + damage + " slashing damage.")
        dice.show_attack(to_hit, damage)
