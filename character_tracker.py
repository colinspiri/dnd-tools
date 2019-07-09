import jsonloader as loader
from pc import PC
import parser
from initiative import Initiative

requested_pc = input("Which player character do you want to use? ").strip().lower()
pc = PC(loader.get_pc(requested_pc))
print("Got statistics for " + pc.name)
print()
print(pc)

initiative = Initiative()
initiative.add_entity(pc, 1)

while(True):
    parser.get_input(initiative)
    print()
