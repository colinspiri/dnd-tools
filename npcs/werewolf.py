from npc import NPC
import dice

class Werewolf(NPC):
    def __init__(self):
        rolls, modifier, result = dice.roll("9d8+18")
        NPC.__init__(self, "Werewolf", result,
        {
        'STR': 15,
        'DEX': 13,
        'CON': 14,
        'INT': 10,
        'WIS': 11,
        'CHA': 10
        }, {})

    def action(self, action_name):
        if "bite" in action_name:
            self.action_bite()
        elif "claw" in action_name:
            self.action_claw()
        elif "spear" in action_name:
            if "two" in action_name or "2" in action_name or "strong" in action_name:
                self.action_spear_strong()
            else:
                self.action_spear_light()
        else:
            print("Action name not recognized.")
    def action_bite(self):
        to_hit = "+4"
        damage = "1d8+2"
        print(self.name + " attacks with " + to_hit + " to hit for " + damage + " piercing damage.")
        dice.show_attack(to_hit, damage)
        print("If the target is a humanoid, it must succeed on a DC 12 CON saving throw or be cursed with werewolf lycanthropy.")
    def action_claw(self):
        to_hit = "+4"
        damage = "2d4+2"
        print(self.name + " attacks with " + to_hit + " to hit for " + damage + " slashing damage.")
        dice.show_attack(to_hit, damage)
    def action_spear_strong(self):
        to_hit = "+4"
        damage = "1d8+2"
        print(self.name + " attacks with " + to_hit + " to hit for " + damage + " piercing damage. (two-handed)")
        dice.show_attack(to_hit, damage)
    def action_spear_light(self):
        to_hit = "+4"
        damage = "1d6+2"
        print(self.name + " attacks with " + to_hit + " to hit for " + damage + " piercing damage. (one-handed/ranged)")
        dice.show_attack(to_hit, damage)
