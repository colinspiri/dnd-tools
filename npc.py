from creature import Creature
import dice
import jsonloader as loader


class NPC(Creature):
    def __init__(self, json_object):
        _, _, max_hit_points = dice.roll(json_object["max_hit_points"])

        Creature.__init__(self, max_hit_points, json_object["actions"], json_object)

        self.current_hit_points = self.max_hit_points


if __name__ == "__main__":
    npc = NPC(loader.get_creature("strahd"))
    print(npc.saving_throws)
    npc.action("bite")
