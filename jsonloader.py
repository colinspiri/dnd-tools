import json

# retrieves creature from json file and returns it as an object
def get_creature(creature_name):
    with open("creatures.json", "r") as file:
        data = json.load(file)
        creature = data[creature_name]
        creature["dead"] = False
        print("Successfully retrieved " + creature_name + " stats from JSON.")
        return creature

if __name__ == "__main__":
    druid = get_creature("druid")
    actions = druid["actions"]["quarterstaff"]["to_hit"]
    print(druid)
