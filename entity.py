
class Entity:
    def __init__(self, name):
        self.name = name
        self.damage_taken = 0
        self.dead = False

    def take_damage(self, damage):
        self.damage_taken += damage
        if hasattr(self, 'max_hit_points'):
            if self.damage_taken >= self.max_hit_points:
                print(self.name + " has taken damage exceeding their max hit points. Use 'remove' to consider them dead.")
        if self.damage_taken < 0:
            self.damage_taken = 0

    def heal(self, damage):
        self.take_damage(-damage)

    def __str__(self):
        return self.name + " has taken " + str(self.damage_taken) + " damage."
