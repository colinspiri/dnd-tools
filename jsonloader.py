import json


def update_pcs(pcs):
    data = None
    with open("data/pcs.json", "r") as file:
        data = json.load(file)
        for json_pc_key, json_pc in data.items():
            for pc in pcs:
                if json_pc["name"] == pc.name:
                    data[json_pc_key] = pc.json_object
                    print("Stored all data for " + pc.name + " in JSON.")
    with open("data/pcs.json", "w") as file:
        json.dump(data, file, indent=2)


def get_class_features(requested_class, max_level):
    with open("data/classes.json", "r") as file:
        data = json.load(file)
        features = {}
        for i in range(max_level):
            for feature_name, feature in data[requested_class]["features"][i].items():
                features[feature_name] = feature
        return features


def get_npc(requested_npc):
    with open("data/npcs.json", "r") as file:
        data = json.load(file)
        for npc_name, npc in data.items():
            if npc_name == requested_npc:
                return npc
            try:
                for command in npc["commands"]:
                    if command == requested_npc:
                        return npc
            except Exception:
                pass


def get_json_object(requested_json_object, file_name):
    with open(file_name, "r") as file:
        data = json.load(file)
        for json_object_name, json_object in data.items():
            if json_object_name == requested_json_object:
                return json_object


def get_pc(requested_pc):
    return get_json_object(requested_pc, "data/pcs.json")


def get_weapon(requested_weapon):
    return get_json_object(requested_weapon, "data/weapons.json")


def get_command_names():
    with open("data/commands.json", "r") as file:
        data = json.load(file)
        command_names = []
        for command_name in data:
            command_names.append(command_name)
        return command_names


def get_command_description(requested_command):
    return get_json_object(requested_command, "data/commands.json")


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
