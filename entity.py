
class Entity:
    def __init__(self, name):
        self.name = name
        self.damage_taken = 0
        self.dead = False

    def take_damage(self, damage):
        self.damage_taken += damage
        if hasattr(self, 'current_hit_points'):
            self.current_hit_points -= damage
            if self.current_hit_points <= 0:
                print(self.name + " has dropped to " + str(self.current_hit_points) + " hit points. Use the 'remove' command to consider them dead.")
    def heal(self, damage):
        self.damage_taken -= damage
        if hasattr(self, "current_hit_points"):
            self.current_hit_points += damage
            if self.current_hit_points > self.max_hit_points:
                self.current_hit_points = self.max_hit_points
                self.damage_taken = 0

    def __str__(self):
        return self.name + " has taken " + str(self.damage_taken) + " damage."
