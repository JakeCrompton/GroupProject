import json, os, pygame, sys, time

base_path = os.path.dirname(__file__) # finds the directory for the files
mapFile = os.path.join(base_path, "mapLoader.json")
saveFIle = os.path.join(base_path, "savefile.json")

with open(mapFile, "r") as file:
    mapData = json.load(file) # loads the json file as a variable

current_location = mapData['player']['start_location']
current_floor = mapData['player']['start_floor']

# Functions
def clearOutput(): # call this function when you want to clear whatever is in the output (cleans it up)
    os.system('cls')

def commands(playerInput, current_location, current_floor):
    words = playerInput.lower().split()
    command = words[0]
    arguement = words[1]

    actions = {
        "go": go,
        "drop": drop,
        "inventory": inventory,
    }    

    if command in actions:
        actions[command](arguement, mapData, current_location, current_floor)
    else:
        print("Invalid input")

def go(direction, mapData, current_location, current_floor):
    try:
        print(f"You are trying to move {direction} to {mapData[current_floor][current_location]['exits'][direction]}")
    except KeyError:
        print("Not a valid direction")

def inventory():
    print("Inventory function")

def drop(item):
    print("drop function")

def save_game():
    print("save function")

# Main loop
while True:
    clearOutput()
    print(f"You are currently at {current_location} on the {current_floor}")

    exits = mapData[current_floor][current_location]['exits']
    print("Exits: ")
    for direction, room in exits.items():
        print(f"->    {direction.capitalize()} to {room}")

    print("\nWhat would you like to do?")
    choice = input("> ")
    commands(choice, current_location, current_floor)
    time.sleep(5)