import json, os, sys, time, random

base_path = os.path.dirname(__file__) # finds the directory for the files 
mapFile = os.path.join(base_path, "mapLoader.json")
saveFile = os.path.join(base_path, "savefile.json")
npcs = os.path.join(base_path, "npcs.json")

CurrentEnemy = {}
EnemyInRoom = []

with open(mapFile, "r") as file:
    mapData = json.load(file) # loads the json file as a variable

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
        "help": helpCommand,
        "speak": TalkTo
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

def shop(arugment, mapData, current_location, current_floor):
    print("Shop")

def save_game(arugment, mapData, current_location, current_floor):
    print("Save game")

def zombieHandler():
    EnemyInRoom.clear() # reset room each time
    amount = random.randint(1,5)

    for i in range(amount):
        UpdatedLabel = "Zombie " + str(i + 1)
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

            CurrentEnemy.update({
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

def helpCommand(argument, mapData, current_location, current_floor):
    print("Available commands:")
    print("-    go <direction> | Move to another room (e.g. 'go north')")
    print("-    inventory | Show what items you have")
    print("-    pickup <item> | Pick up an item")
    print("-    drop <item> | Drop an item that you have in your inventory")
    print("-    help | Show this help list")
    return current_location

def loadSave():
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
    #zombieHandler()

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