import json, os, pygame, sys, time

base_path = os.path.dirname(__file__) # finds the directory for the files
mapFile = os.path.join(base_path, "mapLoader.json")


with open(mapFile, "r") as file:
    mapData = json.load(file) # loads the json file as a variable

player_location = mapData['player']['start_location'] # gets player data
player_square = mapData['player']['start_square']
inventory = mapData['player']['inventory']

# Functions
def clearOutput(): # call this function when you want to clear whatever is in the output (cleans it up)
    os.system('cls')

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
        player_square = next_room_data['room_start_square'] # changes the players square to the door of the next room
        print(f"You are now on the square {player_square}")
        return new_room
    
    else:
        print("You cannot move that way")
        return player_location

def moveSquare(direction, player_square, player_location, mapData):  # in this function is where it will check if the square is a door or sum (still need to add it but it works just not well)
    count = 0
    for i in current_room['room_size']:
        if player_square[count] >= i:
            print("You cannot move that way because youll be in the wall")
            didNotMove = True
            print(player_square)
            time.sleep(2)
            return didNotMove
    if direction == "up":  # do for loop instead
        player_square[0] += 1
        print(f"Moved up a square. Current square: {player_square}")
        didNotMove = False
        time.sleep(2)
        return didNotMove 
    elif direction == "down":
        player_square[0] -= 1
        print(f"Moved down a square. Current square: {player_square}")
        didNotMove = False
        time.sleep(2)
        return didNotMove 
    elif direction == "right":
        player_square[1] += 1
        print(f"You move right a square. Current square: {player_square}")
        didNotMove = False
        time.sleep(2)
        return didNotMove 
    elif direction == "left":
        player_square[1] -= 1
        print(f"You moved left a square. Current square: {player_square}")
        didNotMove = False
        time.sleep(2)
        return didNotMove 
    time.sleep(500)

# Main
didNotMove = True
validDirection = ["up", "down", "right", "left"]
while didNotMove == True:
    clearOutput()
    current_room = mapData['Rooms'][player_location]
    print("Which direction would you like to go?")
    for i in validDirection:
        print(f"{i}")
    direction = input("> ").strip().lower()
    if direction in validDirection:
        player_square = moveSquare(direction, player_square, player_location, mapData)
    else:
        print("Invalid option")
        time.sleep(3)



changeRoom = False
while changeRoom == True:
    clearOutput()
    current_room = mapData['Rooms'][player_location] # get info about new room
    print(f"\n{current_room['description']}: {player_location}")
    
    print("Where would you like to go?")
    for direction, room in current_room['exits'].items():
        print(f"-    {direction}: {room}")
    direction = input("> ").strip().lower()

    player_location = moveRoom(direction, player_location, mapData)
    current_room = mapData['Rooms'][player_location]
    time.sleep(20)