import json, os, sys, time, random

base_path = os.path.dirname(__file__) # finds the directory for the files 
mapFile = os.path.join(base_path, "mapLoader.json")
saveFile = os.path.join(base_path, "savefile.json")
npcs = os.path.join(base_path, "npcs.json")
upgrades = os.path.join(base_path, "upgrades.json")

CurrentEnemy = {} # defining the dictionary and list so that the enemies can reset when ran
EnemyInRoom = []

with open(mapFile, "r") as file:
    mapData = json.load(file) # loads the json file as a variable

with open(upgrades, "r") as file:
    upgradesData = json.load(file)

current_location = mapData['player']['start_location']  # this part of the code is where the save file could come in
current_floor = mapData['player']['start_floor']
player_inventory = mapData['player']['inventory']

# Functions
def clearOutput(): # call this function when you want to clear whatever is in the output (cleans it up)
    """
    DOESNT WORK ON MAC NEED TO FIX THIS 
    """
    os.system('cls')

def commands(playerInput, current_location, current_floor):
    """
    This function takes the players input as the parameter and then splits up their input to check if it is valid, this is done by checking their input against the a dictionary with the function names so that they can be called
    """
    words = playerInput.lower().split() # splits players inputted words into a list

    if len(words) >= 2 and words[0] == "pick" and words[1] == "up": # this will join the words if they are pick up
        command = "pickup"
        arguement = " ".join(words[2:]) if len(words) > 2 else None
    else:
        command = words[0] # This sets the command (function) as the first position from words and the rest will be the argument such as "go {direction}", go is the command and direction is the argument
        arguement = " ".join(words[1:]) if len(words) > 1 else None

    actions = {  # dictionary of all the valid commands
        "go": go,
        "drop": drop,
        "pickup": pickUp,
        "inventory": inventory,
        "help": helpCommand,
        "speak": TalkTo,
        "shop": shop
    }    

    if command in actions: # checks that the command is valid
        return actions[command](arguement, mapData, current_location, current_floor) # this runs the function with the specified input
    else:
        print("Invalid input")
        return current_location

def go(direction, mapData, current_location, current_floor):
    """
    This function will be called when the player inputs "go {direction}", the function takes the parameters of the direction and the players current location and will check it against all the valid exists in the JSON file
    """
    global player_inventory

    try:
        new_location = mapData[current_floor][current_location]['exits'][direction] # This tries to update the players location using try except, if it fails that means the direction the player wants to move is not valid
        required_items = mapData[current_floor][new_location].get('required_items', []) # Check if an item is required to go into a place 

        if required_items: # This will display the required items to the player if they do not have them in their inventory
            for item in required_items:
                if item not in player_inventory:
                    print(f"You cannot enter {new_location} without {item}")
                    return current_location # returns their original position because they didnt have the required items
                
        print(f"You have moved to {new_location}")
        return new_location
    
    except KeyError: # Error handling because if the player doesnt enter a valid direction it will give an error
        print("Not a valid direction")
        return current_location

def inventory(argument, mapData, current_location, current_floor):
    """
    This is the inventory function, this is where the player can check what items they have
    """
    maxItems = 5

    if len(player_inventory) > 5:
        print("Inventory too much")

    print("You currently have:")
    for i in player_inventory:
        print(i)

    return current_location

def drop(item, mapData, current_location, current_floor):
    """
    The drop function allows the player to drop items that they have in their inventory onto the floor, the location the item was dropped in stays there
    """
    item = item.capitalize()

    if item not in player_inventory: # checks if the item is in the players inventory
        print("That item is not in your inventory")
        return current_location
    
    else: # If the item is in their inventory:
        print(f"Dropped {item} in {current_location}")
        player_inventory.remove(item)  # This will drop the item and add it to the mapData where the item can be saved to that location so the player can come back and interact with it again
        mapData[current_floor][current_location]['items'].append(item)

    return current_location

def pickUp(item, mapData, current_location, current_floor):
    """
    This function works similar to the drop function, when the player is in a location that has an item within it, it will prompt the player and if they pick it up it will remove it from the items list that the location has
    """
    item = item.capitalize()
    if len(player_inventory) >= 5:
        print("Your inventory is too full")

    for i in mapData[current_floor][current_location]['items']: # This will print all of the items within the room the player is currently in
        if i == item:
            player_inventory.append(item)  # This adds the item to the players inventory
            mapData[current_floor][current_location]['items'].remove(item) # This will remove the item off of the floor so the player can only pick it up once
            print(f"Added {item} to your inventory")
            return current_location
        
    print(f"There is no {item} in this room")
    return current_location

def shop(arugment, mapData, current_location, current_floor):
    print("Welcome to the shop!")
    for item, data in upgradesData['Shop'].items():
        print(f"-   {item}: {data}")

def save_game(arugment, mapData, current_location, current_floor):
    print("Save game")

def zombieHandler():
    """
    """
    EnemyInRoom.clear() # reset room each time
    amount = random.randint(1,5) # Max amount of enemies that can spawn

    for i in range(amount):
        UpdatedLabel = "Zombie " + str(i + 1) # Adds identifier to the zombie (Could make each zombie a dictionary inside a list or similar (have their own profiles then))
        EnemyInRoom.append(UpdatedLabel)

    print(f"{amount} zombies has spawned")
    print(EnemyInRoom)

    print("What would you like to do?")
    choice = input("> ").strip().lower()
    if choice == "fight":
        print("Which one would you like to fight? (enter a number)")
        try:
            choice1 = int(input("> "))
            if choice1 < 1 or choice1 > amount:
                print("That isn't a valid choice")
                return
            
            selected_enemy = EnemyInRoom[choice1 - 1]

            CurrentEnemy.update({  # This updates the current enemy dictionary with their main hp, name and ID to make sure that the combat system will work correctly
                "Name": selected_enemy,
                "Health": 100,
                "ID": choice1 
            })

            print(f"You are fighting: {CurrentEnemy}")

        except ValueError:
            print("Please enter a number")

    elif choice == "run":
        print("You have ran away")
        
    else:
        print("Invalid choice")


def save_game(mapData):
    print("save function") # not sure how to implement this yet

def helpCommand(argument, mapData, current_location, current_floor): # Help function
    print("Available commands:")
    print("-    go <direction> | Move to another room (e.g. 'go north')")
    print("-    inventory | Show what items you have")
    print("-    pickup <item> | Pick up an item")
    print("-    drop <item> | Drop an item that you have in your inventory")
    print("-    help | Show this help list")
    return current_location

def loadSave():
    """
    This will be a feature that will allow the player to load a previous save that they have started
    """
    print("Have you played before?")
    choice = input("> ").lower().strip()
    if choice == "yes":
        print("Welcome back!")
        time.sleep(1)
        print("Would you like to start a New game or Continue?")
        NewOrLoad = input("> ").lower().strip()
        if NewOrLoad == "new game" or NewOrLoad == "new":
            print("Starting New game.")
        else:
            print("Loading your save..")
    else:
        print("Would you like to go through a tutorial?")
        SkipTutorial = input("> ").lower().strip()
        if SkipTutorial == "yes":
            print("Loading tutorial..")
        else:
            print("Skipping...")
    time.sleep(2)

def tutorial():
    clearOutput()
    print("This is the tutorial!")
    print("You will learn everything you need to start your adventure!")

def TalkTo(arugment, mapData, current_location, current_floor):
    print("Trying to talk to an npc")

# Main loop
while True:
    clearOutput()

    print(f"You are currently at {current_location} on the {current_floor}")

    exits = mapData[current_floor][current_location]['exits']  #doesnt check for 2nd floor yet
    print("Exits: ")
    for direction, room in exits.items():
        print(f"->    {direction.capitalize()} to {room}")

    if len(mapData[current_floor][current_location]['items']) > 0:
        print("Items:")
        for items in mapData[current_floor][current_location]['items']:
            print(f"-   {items.capitalize()}")

    print("\nWhat would you like to do?")
    choice = input("> ").lower().strip()
    current_location = commands(choice, current_location, current_floor)

    time.sleep(5)