from creature import Creature
import constants
import dice
import jsonloader as loader

class NPC(Creature):
    def __init__(self, object):
        _, _, max_health = dice.roll(object["max_health"])

        Creature.__init__(self, max_health, object["actions"], object)

        self.current_health = self.max_health

if __name__ == "__main__":
    npc = NPC(loader.get_creature("strahd"))
    print(npc.saving_throws)
    npc.action("bite")
