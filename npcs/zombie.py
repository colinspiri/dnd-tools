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
        }, {
        'WIS': 0
        })

    # Undead Fortitude
    def take_damage(self, damage):
        self.damage_taken += damage
        self.current_health -= damage
        if self.current_health <= 0:
            save_bonus = self.ability_modifiers["CON"]
            save_dc = 5 + damage
            save_success, saving_throw = dice.save(str(save_bonus), str(save_dc))
            if save_success:
                print("After a seemingly fatal blow, " + self.name + "\'s undead fortitude reduced it to 1 hit point instead. (unless the damage was radiant or from a critical hit)")
                self.damage_taken -= abs(1 - self.current_health)
                self.current_health = 1
            else:
                self.dead = True

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
