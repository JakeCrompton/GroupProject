import json, os, pygame, sys

base_path = os.path.dirname(__file__) # finds the directory for the files
mapFile = os.path.join(base_path, "mapLoader.json")


with open(mapFile, "r") as file:
    mapData = json.load(file) # loads the json file as a variable

player_location = mapData['player']['start_location'] # gets player data

inventory = mapData['player']['inventory']

# Functions

def move(direction, player_location, mapData): # checks if the direction the user entered is valid (using a function so easier to run)

    current_room = mapData['Rooms'][player_location]
    
    if direction in current_room['exits']:
        new_room = current_room['exits'][direction]
        print(f"You have moved {direction} to {new_room}")
        return new_room
    else:
        print("You cannot move that way")
        return player_location

# Main
round = 0

while True: 
    current_room = mapData['Rooms'][player_location] # get info about new room
    print(f"\n{current_room['description']}")
    print(f"Items here: {current_room['items']}")
    print(f"Exits: {list(current_room['exits'].keys())}")

    print(f"Where would you like to go? {current_room['exits']}")
    direction = input(">").strip().lower()

    player_location = move(direction, player_location, mapData)
    current_room = mapData['Rooms'][player_location]
    print(f"You are now in {player_location}")

