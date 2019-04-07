
def input_initiative():
    order = []

    # Store input into order
    while True:
        text = input("> ").strip()
        if text == "":
            break
        words = text.split()
        order.append({
            "name": words[0],
            "initiative": int(words[1])
        })

    # Sort order by initiative count
    def getInitiative(elem):
        return elem["initiative"]
    order.sort(key = getInitiative, reverse = True)
    return order

def show_initiative(order):
    print()
    print("Initiative Order: ")
    for turn in order:
        print(turn["name"] + " (" + str(turn["initiative"]) + ")")
    print()

if __name__ == "__main__":
    order = input_initiative()
    show_initiative(order)
    
    # Cycle through order
    current_turn = 0
    while True:
        print(order[current_turn]["name"] + " (" + str(order[current_turn]["initiative"]) + ") is up." )
        text = input("Next? ").strip()
        current_turn += 1
        current_turn %= len(order)
