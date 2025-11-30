# needs fixing - pick up function and command function, the input is case sensitive which we dont want

import json, os, pygame, sys, time

base_path = os.path.dirname(__file__) # finds the directory for the files 
mapFile = os.path.join(base_path, "mapLoader.json")
saveFile = os.path.join(base_path, "savefile.json")

with open(mapFile, "r") as file:
    mapData = json.load(file) # loads the json file as a variable

current_location = mapData['player']['start_location']  # this part of the code is where the save file could come in
current_floor = mapData['player']['start_floor']
player_inventory = mapData['player']['inventory']

# Functions
def clearOutput(): # call this function when you want to clear whatever is in the output (cleans it up)
    os.system('cls')

def commands(playerInput, current_location, current_floor):
    words = playerInput.lower().split()

    if len(words) >= 2 and words[0] == "pick" and words[1] == "up":
        command = "pickup"
        arguement = " ".join(words[2:]) if len(words) > 2 else None
    else:
        command = words[0]
        arguement = " ".join(words[1:]) if len(words) > 1 else None

    actions = {
        "go": go,
        "drop": drop,
        "pickup": pickUp,
        "inventory": inventory,
        "help": helpCommand
    }    

    if command in actions:
        return actions[command](arguement, mapData, current_location, current_floor)
    else:
        print("Invalid input")
        return current_location

def go(direction, mapData, current_location, current_floor):
    global player_inventory

    try:
        new_location = mapData[current_floor][current_location]['exits'][direction]
        required_items = mapData[current_floor][new_location].get('required_items', [])

        if required_items:
            for item in required_items:
                if item not in player_inventory:
                    print(f"You cannot enter {new_location} without {item}")
                    return current_location
        print(f"You have moved to {new_location}")
        return new_location
    
    except KeyError:
        print("Not a valid direction")
        return current_location

def inventory(argument, mapData, current_location, current_floor):
    maxItems = 5

    if len(player_inventory) > 5:
        print("Inventory too much")

    print("You currently have:")
    for i in player_inventory:
        print(i)

    return current_location

def drop(item, mapData, current_location, current_floor):
    item = item.capitalize()
    if item not in player_inventory:
        print("That item is not in your inventory")
        return current_location
    else:
        print(f"Dropped {item} in {current_location}")
        player_inventory.remove(item)
        mapData[current_floor][current_location]['items'].append(item)
    return current_location

def pickUp(item, mapData, current_location, current_floor):
    item = item.capitalize()
    if len(player_inventory) >= 5:
        print("Your inventory is too full")

    for i in mapData[current_floor][current_location]['items']:
        if i == item:
            player_inventory.append(item)
            mapData[current_floor][current_location]['items'].remove(item)
            print(f"Added {item} to your inventory")
            return current_location
        
    print(f"There is no {item} in this room")
    return current_location

def save_game(mapData):
    print("save function")

def helpCommand(argument, mapData, current_location, current_floor):
    print("Available commands:")
    print("-    go <direction> | Move to another room (e.g. 'go north')")
    print("-    inventory | Show what items you have")
    print("-    pickup <item> | Pick up an item")
    print("-    drop <item> | Drop an item that you have in your inventory")
    print("-    help | Show this help list")
    return current_location

# Main loop
while True:
    clearOutput()
    print(f"You are currently at {current_location} on the {current_floor}")

    exits = mapData[current_floor][current_location]['exits']
    print("Exits: ")
    for direction, room in exits.items():
        print(f"->    {direction.capitalize()} to {room}")

    if len(mapData[current_floor][current_location]['items']) > 0:
        print("Items:")
        for items in mapData[current_floor][current_location]['items']:
            print(f"-   {items.capitalize()}")

    print("\nWhat would you like to do?")
    choice = input("> ")
    current_location = commands(choice, current_location, current_floor)

    time.sleep(10)