
class Entity:
    def __init__(self, name):
        self.name = name
        self.damage_taken = 0
        self.dead = False

    def take_damage(self, damage):
        self.damage_taken += damage
        if hasattr(self, 'current_health'):
            self.current_health -= damage
            if self.current_health <= 0:
                print(self.name + " has dropped to " + str(self.current_health) + " hit points. Consider them dead?")
                text = input("> ").strip()
                if text == "y" or text == "yes":
                    self.dead = True
                    print(self.name + " died.")
            elif self.current_health > self.max_health:
                self.current_health = self.max_health
                self.damage_taken = 0

    def __str__(self):
        return self.name + " has taken " + str(self.damage_taken) + " damage."
