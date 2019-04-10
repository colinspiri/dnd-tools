from npc import NPC
import dice

class VampireSpawn(NPC):
    def __init__(self):
        rolls, modifier, result = dice.roll("11d8+33")
        NPC.__init__(self, "Vampire Spawn", result,
        {
        'STR': 16,
        'DEX': 16,
        'CON': 16,
        'INT': 11,
        'WIS': 10,
        'CHA': 12
        }, {
        'DEX': 6,
        'WIS': 3
        })

    def action(self, action_name):
        if "bite" in action_name:
            self.action_bite()
        elif "claw" in action_name:
            self.action_claw()
        else:
            print("Action name not recognized.")
    def action_bite(self):
        to_hit = "+6"
        damage = "1d6+3"
        bonus_damage = "2d6"
        print(self.name + " attacks a grappled creature with " + to_hit + " to hit for " + damage + " piercing damage and " + bonus_damage + " necrotic damage.")
        dice.show_attack(to_hit, damage)
        rolls, modifier, result = dice.roll(bonus_damage)
        print("Bonus Necrotic Damage: " + str(result))
        print("The target's hit point maximum is reduced by " + str(result) + ", and the vampire regains " + str(result) + " hit points. The reduction lasts until the target finishes a long rest. The target dies if this effect reduces its hit point maximum to 0.")
    def action_claw(self):
        to_hit = "+6"
        damage = "2d4+3"
        print(self.name + " attacks with " + to_hit + " to hit for " + damage + " slashing damage.")
        dice.show_attack(to_hit, damage)
        print("Instead of dealing damage, the vampire can grapple the target (escape DC 13).")
