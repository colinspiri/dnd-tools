from npc import NPC
import dice

class Strahd(NPC):
    def __init__(self):
        rolls, modifier, result = dice.roll("17d8+68")
        NPC.__init__(self, "Strahd von Zarovich", result,
        {
        'STR': 18,
        'DEX': 18,
        'CON': 18,
        'INT': 20,
        'WIS': 15,
        'CHA': 18
        }, {
        'DEX': 9,
        'WIS': 7,
        'CHA': 9
        })

    def action(self, action_name):
        if "unarmed" in action_name or "hit" in action_name:
            self.action_unarmed_strike()
        elif "bite" in action_name:
            self.action_bite()
        else:
            print("Action name not recognized.")
    def action_unarmed_strike(self):
        to_hit = "+9"
        damage = "1d8+4"
        bonus_damage = "4d6"
        print(self.name + " attacks with " + to_hit + " to hit for " + damage + " bludgeoning damage and " + bonus_damage + " necrotic damage.")
        dice.show_attack(to_hit, damage)
        rolls, modifier, result = dice.roll(bonus_damage)
        print("Bonus Necrotic Damage: " + str(result))
        print("Instead of dealing the bludgeoning damage, Strahd can grapple the target (escape DC 18).")
    def action_bite(self):
        to_hit = "+9"
        damage = "1d6+4"
        bonus_damage = "3d6"
        print(self.name + " attacks a grappled creature with " + to_hit + " to hit for " + damage + " piercing damage and " + bonus_damage + " necrotic damage.")
        dice.show_attack(to_hit, damage)
        rolls, modifier, result = dice.roll(bonus_damage)
        print("Bonus Necrotic Damage: " + str(result))
        print("The target's hit point maximum is reduced by " + str(result) + ", and Strahd regains " + str(result) + " hit points. The reduction lasts until the target finishes a long rest. The target dies if this effect reduces its hit point maximum to 0. A humanoid slain in this way may rise as a vampire spawn under Strahd’s control.")
