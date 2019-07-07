import json

def update_pcs(pcs):
    data = None
    with open("pcs.json", "r") as file:
        data = json.load(file)
        for json_pc_key, json_pc in data.items():
            for pc in pcs:
                if json_pc["name"] == pc.name:
                    data[json_pc_key] = pc.json_object
                    print("Stored all data for " + pc.name + " in JSON.")
    with open("pcs.json", "w") as file:
        json.dump(data, file, indent=2)

# retrieves npc from json file and returns it as an object
def get_npc(requested_npc):
    with open("npcs.json", "r") as file:
        data = json.load(file)
        for npc_name, npc in data.items():
            if npc_name == requested_npc:
                # print("Successfully retrieved " + creature_name + " stats from JSON.")
                return npc
            try:
                for command in npc["commands"]:
                    if command == requested_npc:
                        # print("Successfully retrieved " + creature_name + " stats from JSON.")
                        return npc
            except:
                pass

def get_object(requested_object, file_name):
    with open(file_name, "r") as file:
        data = json.load(file)
        for object_name, object in data.items():
            if object_name == requested_object:
                return object

def get_pc(requested_pc):
    return get_object(requested_pc, "pcs.json")

def get_weapon(requested_weapon):
    return get_object(requested_weapon, "weapons.json")

def get_command_names():
    with open("commands.json", "r") as file:
        data = json.load(file)
        command_names = []
        for command_name in data:
            command_names.append(command_name)
        return command_names
def get_command_description(requested_command):
    return get_object(requested_command, "commands.json")

def get_simple_action_dictionary(name, range, to_hit, damage_dice, damage_type):
    return {
    "name": str(name),
    "range": str(range),
    "to_hit": str(to_hit),
    "damage": [
    {
    "damage_dice": str(damage_dice),
    "damage_type": str(damage_type)
    }
    ],
    "effects": []
    }

if __name__ == "__main__":
    command = get_command_description("help")
    print(command)
