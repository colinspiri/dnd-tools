import jsonloader as loader
from pc import PC

# requested_pc = input("Which player character do you want to use? ").strip().lower()
requested_pc = "igor"
pc = PC(loader.get_pc(requested_pc))
print("Got statistics for " + pc.name)
print()
print(pc)
print(pc.actions)
