# If the script doesnt work (says the file doesnt exist or sum) type in "cd yourfilelocation" in the output
# means we can change stuff inside the map and it would work as it would as if it was something else. Can store map data inside the json file such as drops, npcs, enemies and other shit like that

# pygame stuff is just testing rn it will be changed

# importing json and os so it can find the files + pygame for the window (adding pygame back later it was always running and got in the way)
import json, os, pygame, sys

# loads the json map file
base_path = os.path.dirname(__file__)
mapFile = os.path.join(base_path, "mapLoader.json")

# reads the json file 
with open(mapFile, "r") as file:
    mapData = json.load(file)

# MAIN PART BELOW

# rounds of *zombies* that will attack you, you can only move a certain amount of steps inbetween the round but every 5 rounds you can move as much as you want till you choose to resume the game (gives you time to progress with the story, cannot complete the whole story in that time)

def move(direction, player_location, mapData):  # can run this function instead of running it each time the player wants to go to a different room
    current_room = mapData['Rooms'][player_location]
    
    if direction in current_room['exits']:
        new_room = current_room['exits'][direction]
        print(f"You have moved {direction} to {new_room}")
        return new_room
    else:
        print("You cannot move that way")
        return player_location

# gets player data
player_location = mapData['player']['start_location']
inventory = mapData['player']['inventory']

# get info about new room
current_room = mapData['Rooms'][player_location]
print(f"\n{current_room['description']}")
print(f"Items here: {current_room['items']}")
print(f"Exits: {list(current_room['exits'].keys())}")

print(f"Where would you like to go? {current_room['exits']}")
direction = input(">").strip().lower()

player_location = move(direction, player_location, mapData)
current_room = mapData['Rooms'][player_location]
print(f"You are now in {player_location}")
# check if the direction is valid 