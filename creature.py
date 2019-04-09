
class Creature:
    def __init__(self, name):
        self.name = name
        self.damage_taken = 0
        self.dead = False

    def set_initiative(self, initiative):
        self.initiative = initiative

    def take_damage(self, damage):
        self.damage_taken += damage
        if hasattr(self, 'max_health') and self.get_current_health() <= 0:
            self.dead = True

    def __str__(self):
        return self.name + " has taken " + str(self.damage_taken) + " damage."
