from npc import NPC
import dice

class Wolf(NPC):
    def __init__(self):
        rolls, modifier, result = dice.roll("2d8+2")
        NPC.__init__(self, "Wolf", result,
        {
        'STR': 12,
        'DEX': 15,
        'CON': 12,
        'INT': 3,
        'WIS': 12,
        'CHA': 6
        })

    def __str__(self):
        return "Wolf has " + str(self.get_current_health()) + "/" + str(self.max_health) + " health."

if __name__ == "__main__":
    wolf = Wolf()
    print(str(wolf))
