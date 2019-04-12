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

if __name__ == "__main__":
    creature = get_creature("vampire spawn")
    print(creature)
