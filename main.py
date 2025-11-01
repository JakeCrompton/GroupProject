# If the script doesnt work (says the file doesnt exist or sum) type in "cd yourfilelocation" in the output
# means we can change stuff inside the map and it would work as it would as if it was something else (Data wise)

import json, os

# load the json map file
base_path = os.path.dirname(__file__)
mapFile = os.path.join(base_path, "mapLoader.json")

# reads the json file
with open(mapFile, "r") as file:
    mapData = json.load(file)

# get the players starting location and inventory
player_location = mapData["player"]["start_location"]
inventory = mapData["player"]["inventory"]

print(f"You start in the player {player_location}.")
print(f"Your inventory {inventory}")

# get info about the new room
current_room = mapData["Rooms"][player_location]
print(f"\n{current_room['description']}")
print(f"Items here: {current_room['items']}")
print(f"Exits: {list(current_room['exits'].keys())}")

print(f"What direction would you like to go {current_room['exits']}")
direction = input(">")


# check if direction is valid
if direction in current_room['exits']:
    new_room = current_room['exits'][direction]
    player_location = new_room
    print(f"\nYou move {direction} to the {player_location}")
else:
    print("\nYou cannot move that way.")
