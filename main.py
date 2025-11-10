import json, os, pygame, sys, time

base_path = os.path.dirname(__file__) # finds the directory for the files
mapFile = os.path.join(base_path, "mapLoader.json")


with open(mapFile, "r") as file:
    mapData = json.load(file) # loads the json file as a variable

player_location = mapData['player']['start_location'] # gets player data
inventory = mapData['player']['inventory']

# Functions

def moveRoom(direction, player_location, mapData): # checks if the direction the user entered is valid (using a function so easier to run)
    current_room = mapData['Rooms'][player_location]

    if direction in current_room['exits']:
        new_room = current_room['exits'][direction]
        next_room_data = mapData['Rooms'][new_room]

        if "required_items" in next_room_data: # checks if there is a required item to go into the next room
            required_items = next_room_data['required_items']
            missing = [item for item in required_items if item not in inventory]
            if missing:
                print(f"To go into {new_room} you need the following items:")
                for item in missing:
                    print(f"- {item}")
                return player_location
            
        print(f"You have moved {direction} to {new_room}")
        return new_room
    
    else:
        print("You cannot move that way")
        return player_location
    
def clearOutput(): # call this function when you want to clear whatever is in the output (cleans it up)
    os.system('cls')

# Main
while True: 
    clearOutput()
    current_room = mapData['Rooms'][player_location] # get info about new room
    print(f"\n{current_room['description']}: {player_location}")
    
    print("Where would you like to go?")
    for direction, room in current_room['exits'].items():
        print(f"-    {direction}: {room}")
    direction = input("> ").strip().lower()

    player_location = moveRoom(direction, player_location, mapData)
    current_room = mapData['Rooms'][player_location]
    time.sleep(2)