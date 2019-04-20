import json

# retrieves creature from json file and returns it as an object
def get_creature(requested_creature):
    with open("creatures.json", "r") as file:
        data = json.load(file)
        for creature_name, creature in data.items():
            if creature_name == requested_creature:
                print("Successfully retrieved " + creature_name + " stats from JSON.")
                return creature
            try:
                for command in creature["commands"]:
                    if command == requested_creature:
                        print("Successfully retrieved " + creature_name + " stats from JSON.")
                        return creature
            except:
                pass

def get_command_names():
    with open("commands.json", "r") as file:
        data = json.load(file)
        command_names = []
        for command_name in data:
            command_names.append(command_name)
        return command_names

def get_command_description(requested_command):
    with open("commands.json", "r") as file:
        data = json.load(file)
        for command_name, command_description in data.items():
            if command_name == requested_command:
                return command_description

if __name__ == "__main__":
    command = get_command_description("help")
    print(command)
