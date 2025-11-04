# If the script doesnt work (says the file doesnt exist or sum) type in "cd yourfilelocation" in the output
# means we can change stuff inside the map and it would work as it would as if it was something else (Data wise)

# importing Datasets 
import json, os, pygame

# importing json and os so it can find the files + pygame for the window
import json, os

# loads the json map file
base_path = os.path.dirname(__file__)
mapFile = os.path.join(base_path, "mapLoader.json")

# reads the json file 
with open(mapFile, "r") as file:
    mapData = json.load(file)

# gets player data
player_location = mapData['player']['start_location']
inventory = mapData['player']['inventory']

print(f"You will start in {player_location}")
print(f"you have {inventory} in your inventory")

# get info about new room
current_room = mapData['Rooms'][player_location]
print(f"\n{current_room['description']}")
print(f"Items here: {current_room['items']}")
print(f"Exits: {list(current_room['exits'].keys())}")

print(f"Where would you like to go? {current_room['exits']}")
direction = input(">").strip().lower()

# check if the direction is valid
if direction in current_room['exits']:
    new_room = current_room['exits'][direction]
    player_location = new_room
    print(f"\nYou have moved {direction} to the {player_location}")
    if current_room["items"]:  # THIS WAS JUST TO TEST ADDING ITEMS (still not finished, adds the [''] to the item)
        inventory.insert(0, current_room["items"])
        print(f"Added {current_room['items']} to your inventory")
        print(f"This is your inventory now: {inventory}")  # FIX THIS 
else:
    print("You cannot move that way")