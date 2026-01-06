import json, os, sys, time, random

base_path = os.path.dirname(__file__) # finds the directory for the files 
mapFile = os.path.join(base_path, "mapLoader.json")
saveFile = os.path.join(base_path, "savefile.json")
npcs = os.path.join(base_path, "npcs.json")
shopFile = os.path.join(base_path, "shop.json")
playerFile = os.path.join(base_path, "player.json")
items = os.path.join(base_path, "items.json")

CurrentEnemy = {} # defining the dictionary and list so that the enemies can reset when ran
EnemyInRoom = []

with open(mapFile, "r") as file:
    mapData = json.load(file) # loads the json file as a variable

with open(shopFile, "r") as file:
    shopData = json.load(file) # This is the shop file

with open(npcs, "r") as file:
    npcData = json.load(file)["Enemies"] # Loads in NPCs

with open(playerFile, "r") as file:
    playerData = json.load(file) # Loading player data into the program

with open (items, "r") as file:
    itemsData = json.load(file)

PlayerInfo = playerData["PlayerInfo"]
PlayerStats = playerData["PlayerStats"]
PlayerSkills = playerData["PlayerSkills"]
Equipped = playerData["Equipped"]

current_location = mapData['player']['start_location']  # this part of the code is where the save file could come in
current_floor = mapData['player']['start_floor']
player_inventory = mapData['player']['inventory']

# Functions
def clearOutput(): # call this function when you want to clear whatever is in the output (cleans it up)
    os.system('cls' if os.name == 'nt' else 'clear')

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
        "shop": shop,
        "save": save_game,
    }    

    if command in actions: # checks that the command is valid
        return actions[command](arguement, mapData, current_location, current_floor) # this runs the function with the specified input
    else:
        print("Invalid input")
        return current_location, current_floor

def go(direction, mapData, current_location, current_floor):
    """
    This function will be called when the player inputs "go {direction}", the function takes the parameters of the direction and the players current location and will check it against all the valid exists in the JSON file
    """
    global player_inventory

    try:
        exits = mapData[current_floor][current_location]['exits'] # All the valid exits for the current room

        if direction not in exits: # Checks if the direction is a real exit
            print("Not a valid direction")
            return current_location, current_floor
        
        destination = exits[direction]

        if destination in mapData: # Checking that the destination is in mapData (valid location)
            new_floor = destination
            new_location = mapData[new_floor]['start_location']

            print(f"You have moved to the {new_floor}")
            return new_location, new_floor
        
        if destination in mapData[current_floor]:
            required_items = mapData[current_floor][destination].get('required_items', [])

            for item in required_items: # If there is a required item for the room it will display it to the user if they do not have it
                if item not in player_inventory:
                    print(f"You cannot enter {destination} without {item}")
                    return current_location, current_floor
                
            print(f"You move to {destination}")
            room = mapData[current_floor][destination]
            min_enemies = room.get('minAmountOfEnemies')
            max_enemies = room.get('maxAmountOfEnemies')

            spawn_enemies(min_enemies, max_enemies)
            return destination, current_floor
        
        print("That location does not exist.")
        return current_location, current_floor
    
    except KeyError as e:  # Error handling incase the player goes to a different direction
        print("Movement error:", e)
        return current_location, current_floor

def inventory(argument, mapData, current_location, current_floor):
    while True:
        clearOutput()

        if len(player_inventory) >= 5:
            print("Your inventory is full")

        if len(player_inventory) == 0:
            print("You have nothing in your inventory")
            time.sleep(2)
            return current_location, current_floor
        
        print("You currently have:")
        for item, quantity in player_inventory.items():
            print(f"{quantity}x - {item}")

        print("Do you want to use an item? (yes, no)")
        choice = input("> ").lower().strip()

        if choice in ("back", "no"):
            return current_location, current_floor
        
        if choice != "yes":
            print("Invalid input")
            time.sleep(1)
            continue

        while True:
            print("Which item would you like to use? (type 'back' to return)")
            item_input = input("> ").strip()

            if item_input.lower() == "back":
                break

            item_name = item_input.capitalize()

            if item_name not in player_inventory:
                print("You dont have that item")
                continue

            if item_name in itemsData['Weapons']:
                print("You equipped a new weapon")

            elif item_name in itemsData['Armour']:
                armour = itemsData['Armour'][item_name]
                slot = armour['Slot']
                defence = armour['Defence']

                if Equipped[slot] != 0:
                    old_armour = Equipped[slot]
                    old_def = itemsData['Armour'][old_armour]['Defence']
                    PlayerStats['Defence'] -= old_def
                    print(f"You unequipped {old_armour}")

                Equipped[slot] = item_name
                PlayerStats['Defence'] += defence

                print(f"You equipped {item_name} in {slot} (+{defence} Defence)")

            elif item_name in itemsData['Potions']:
                heal = itemsData['Potions'][item_name]['Health Regeneration']
                PlayerInfo['Health'] = min(
                    PlayerInfo['Health'] + heal,
                    PlayerInfo['Max Health']
                )
                print(f"You used {item_name} and regained {heal} health")

                player_inventory[item_name] -= 1
                if player_inventory[item_name] <= 0:
                    del player_inventory[item_name]
            else:
                print("That item cannot be used")
                continue

            return current_location, current_floor

def drop(item, mapData, current_location, current_floor):
    """
    The drop function allows the player to drop items that they have in their inventory onto the floor, the location the item was dropped in stays there
    """
    item = item.capitalize()

    if item not in player_inventory: # checks if the item is in the players inventory
        print("That item is not in your inventory")
        return current_location, current_floor
    
    else: # If the item is in their inventory:
        print(f"Dropped {item} in {current_location}")
        player_inventory[item] -= 1  # This will drop the item and add it to the mapData where the item can be saved to that location so the player can come back and interact with it again
        if player_inventory[item] <= 0:
            del player_inventory[item]
        mapData[current_floor][current_location]['items'].append(item)

    return current_location, current_floor

def pickUp(item, mapData, current_location, current_floor):
    """
    This function works similar to the drop function, when the player is in a location that has an item within it, it will prompt the player and if they pick it up it will remove it from the items list that the location has
    """
    item = item.capitalize()
    if sum(player_inventory.values()) >= 5: # Checks to see if players inventory is full
        print("Your inventory is too full")
        return current_location, current_floor
    
    room_items = mapData[current_floor][current_location]['items']

    if item not in room_items:
        print(f"There is no {item} in this room")
        return current_location, current_floor
    
    player_inventory[item] = player_inventory.get(item, 0) + 1
    room_items.remove(item)

    print(f"Added {item} to your inventory")
    return current_location, current_floor

def shop(arugment, mapData, current_location, current_floor):
    clearOutput()
    print("Welcome to the shop!")
    print(f"You currently have {PlayerInfo['Money']} coins")
    time.sleep(0.5)
    inShop = True
    while inShop == True:
        print("What would you like to view?")

        for item, data in shopData['Shop'].items(): # This displays the different offers to the user
            print(f"-   {item}")

        purchase_option = input("> ").lower().strip()
        if purchase_option == "go back" or purchase_option == "back": # This is to check if the user ever wants to go back
            return current_location, current_floor

        if purchase_option.capitalize() not in shopData['Shop']: # Checks to see if input is for sale
            print("Invalid input")
            time.sleep(1)
            clearOutput()
            continue

        clearOutput()
        print(f"This is currently what {purchase_option.capitalize()} we have")

        try:
            for item, values in shopData['Shop'][purchase_option.capitalize()].items(): # displays the items for sale with the stats of them
                print(f"-   {item} {values}")

        except KeyError: # Error handling incase the user inputs something not correct
            print("Invalid input")

        print("What do you want to do?")
        shop_dialog = input("> ").lower().strip()
        shopWords = shop_dialog.split() # splits the words up so that it can be error checked and can go back to main menu with it

        if shopWords[0] == "buy":   
            if PlayerInfo["Money"] >= shopData['Shop'][purchase_option.capitalize()][shopWords[1].capitalize()]['Price']: # Checks to see if the user has enough money to buy the item
                if shopData['Shop'][purchase_option.capitalize()][shopWords[1].capitalize()]['Quantity'] > 0: # Checks if that the item is in stock
                    item_name = shopWords[1].capitalize()
                    player_inventory[item_name] = player_inventory.get(item_name, 0) + 1 # Adds item to inventory
                    print(f"You have bought {shopWords[1].capitalize()}. Item has been added to your inventory")
                    shopData['Shop'][purchase_option.capitalize()][shopWords[1].capitalize()]['Quantity'] -= 1 # Removes 1 off the quantity amount
                    
                    if shopData['Shop'][purchase_option.capitalize()][shopWords[1].capitalize()]['Quantity'] <= 0:
                        shopData['Shop'][purchase_option.capitalize()].pop(shopWords[1].capitalize())
                    print("If you wish to go back, please type 'go back' but if you wish to stay type anything else")
                    shoppingOrBack = input("> ").lower().strip()

                    if shoppingOrBack == "go back":
                        return current_location, current_floor
                    clearOutput()
                else:
                    if shopData['Shop'][purchase_option.capitalize()][shopWords[1].capitalize()] <= 0:
                        shopData['Shop'][purchase_option.capitalize()][shopWords[1].capitalize()].pop(shopWords[1].capitalize())
            else:
                print("You do not have enough money for that")
        elif shopWords[0] == "go" and shopWords[1] == "back":
            inShop = False
            return current_location, current_floor      
        elif shopWords[0] == "back":
            inShop = False
            return current_location, current_floor      
        else:
            print("Invalid input. (Go back or buy)")

    return current_location, current_floor

def save_game(arugment, mapData, current_location, current_floor):
    print("Save game")

def spawn_enemies(min_amount, max_amount):
    EnemyInRoom.clear() # clears the room every time it is called so it doesnt have previous data inside it

    if min_amount is None or max_amount is None:
        return

    amount = random.randint(min_amount, max_amount)

    for i in range(amount):  
        enemy = random.choice(npcData).copy()
        EnemyInRoom.append(enemy)

    if amount > 0:
        fight_enemy(enemy)

def fight_enemy(enemy):
    time.sleep(0.5)
    clearOutput()
    CanRun = True 
    print(f"A {enemy['Name']} wants to fight you!")
    enemyDefeated = False

    while not enemyDefeated:
        if CanRun == True:
            print("What will you do? [fight, items, run]")
        else:
            print("What will you do? [fight, items]")

        fight_option1 = input("> ").lower().strip()

        if fight_option1 == "fight":
            time.sleep(0.5)

            if PlayerStats["Speed"] >= enemy['Speed']:
                print("You have the first move.")

            else:
                print(f"The {enemy['Name']} is faster than you")
            print(f"What move would you like to use on the {enemy['Name']}")

            for skill, dmg in PlayerSkills.items():  # displays the current options for the player when they choose to fight
                print("Skills:")
                print(f"-   {skill}: {dmg} Damage")

            chosen_skill = input(">  ").strip().lower()
            if chosen_skill in (skill.lower() for skill in PlayerSkills):
                playerFirst = PlayerStats['Speed'] >= enemy['Speed']  # Checks to see if the enemy or the player is faster to determine who has the first move

                if playerFirst:  # Player attacks
                    damageDealt = PlayerSkills[chosen_skill.capitalize()] * PlayerStats["Strength"]
                    enemy['Health'] -= damageDealt
                    print(f"You used {chosen_skill.capitalize()} and dealt {damageDealt} damage! The {enemy['Name']} has {enemy['Health']}hp remaining")

                    if enemy['Health'] <= 0:
                        print(f"The {enemy['Name']} has been defeated!")
                        enemyDefeated = True
                        break

                enemy_damage = enemy['Damage']
                PlayerInfo['Health'] -= enemy_damage
                time.sleep(0.5)
                clearOutput()
                print(f"The {enemy['Name']} attacks you for {enemy_damage} damage! {PlayerInfo['Health']} hp remaining.")
                time.sleep(1)

                if not playerFirst:
                    damageDealt = PlayerSkills[chosen_skill.capitalize()] * PlayerStats["Strength"]
                    enemy['Health'] -= damageDealt
                    print(f"You used {chosen_skill.capitalize()} and dealt {damageDealt} damage! The {enemy['Name']} has {enemy['Health']}hp remaining")
                    time.sleep(0.5)

                    if enemy['Health'] <= 0:
                        print(f"The {enemy['Name']} has been defeated!")
                        enemyDefeated = True
                        PlayerInfo["Money"] += enemy['Cash']
                        print(f"You found {enemy['Cash']} coins on the {enemy['Name']}")
                        add_experience(enemy['XP'])
                        return current_location, current_floor

                if PlayerInfo['Health'] <= 0:
                    print("You were defeated.")
                    break # ADD LOSE CONDITION HERE (MAYBE YOU CAN HAVE 1 EXTRA LIFE)

            else:
                print("Invalid skill, try again")

        elif fight_option1 == "run":
            if not CanRun:
                print("You cannot run anymore!")
                continue
            
            chance = random.randint(1, 5)
            if chance != 5:
                print(f"You have successfully ran away from the {enemy['Name']}")
                return current_location, current_floor

            else:
                print("You have failed to run away, you cannot run away from this fight anymore.")
                
                CanRun = False
        elif fight_option1 == "items":
            print("You check your bag...")
            time.sleep(1)

            print(f"What items would you like to use?")
            print("Your current items:")
            for item, quantity in player_inventory.items():
                print(f"- {quantity}x     {item}")

            chosen_item = input("> ").lower().strip()
            if chosen_item.capitalize() in player_inventory:
                if chosen_item.capitalize() in itemsData['Potions']:
                    PlayerInfo['Health'] += itemsData['Potions'][chosen_item.capitalize()]['Health Regeneration']
                    print(f"You have used a {chosen_item} and regained {itemsData['Potions'][chosen_item.capitalize()]['Health Regeneration']} health")
                   
                    if PlayerInfo['Health'] > PlayerInfo['Max Health']:
                        PlayerInfo['Health'] = 100
                        
                    player_inventory[chosen_item.capitalize()] -= 1
                    if player_inventory[chosen_item.capitalize()] <= 0:
                        player_inventory.pop(chosen_item.capitalize())
                else:
                    print("You cannot use that item")
            else:
                print("You do not have that item") 

def helpCommand(argument, mapData, current_location, current_floor): # Help function
    print("Available commands:")
    print("-    go <direction> | Move to another room (e.g. 'go north')")
    print("-    inventory | Show what items you have")
    print("-    pickup <item> | Pick up an item")
    print("-    drop <item> | Drop an item that you have in your inventory")
    print("-    help | Show this help list")
    return current_location, current_floor

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
    return current_location, current_floor
    
def add_experience(amount):
    PlayerInfo["Experience"] += amount
    print(f"You have gained {amount}xp!")
    while PlayerInfo["Experience"] >= xp_to_lvlup(PlayerInfo["Level"]):
        PlayerInfo["Experience"] -= xp_to_lvlup(PlayerInfo["Level"])
        PlayerInfo["Level"] += 1
        PlayerInfo["Stat Points"] += 1
        print(f"Level up! You are now level {PlayerInfo['Level']}!")
        print(f"You have {PlayerInfo['Stat Points']} unspent skill points.")
        # make sure to increase all player stats naturally when they level up too (also regen hp when they level up)
    print(f"Level {PlayerInfo['Level']} {PlayerInfo['Experience']}xp/{xp_to_lvlup(PlayerInfo['Level'])}xp")
    return current_location, current_floor, spend_skill_point(PlayerInfo['Stat Points'])

def xp_to_lvlup(level):
    return 100 * (level + 1) # can change the amount of xp needed by changing the values (100 xp per level)

def spend_skill_point(skillpoints):
    print(f"What would you like to put your {skillpoints} skill points into?")
    for ind in PlayerStats.items():
        print(f"-   {ind}")
    spendSkillPoint = input("> ").lower().strip()
    if spendSkillPoint.capitalize() in PlayerStats:
        PlayerStats[spendSkillPoint.capitalize()] + 1
        print(f"You have increased your {spendSkillPoint} by 1!")
        if spendSkillPoint == "health":
            PlayerInfo['Max Health'] += 20
            PlayerInfo['Health'] += 20
    else:
        print("Invalid input")
    time.sleep(5)
    return current_location, current_floor

# Main loop
while True:
    clearOutput()
    
    print(f"You are currently at {current_location} on the {current_floor}")

    location_data = mapData[current_floor].get(current_location)
    if not location_data or 'exits' not in location_data:
        print("Error: Invalid location data")
        print("Floor:", current_floor)
        print("Location:", current_location)
        break

    exits = location_data['exits']
    print("Exits: ")
    for direction, room in exits.items():
        print(f"->    {direction.capitalize()} to {room}")

    if len(mapData[current_floor][current_location]['items']) > 0:
        print("Items in room:")
        for items in mapData[current_floor][current_location]['items']:
            print(f"-   {items.capitalize()}")

    print("\nWhat would you like to do?")
    choice = input("> ").lower().strip()
    current_location, current_floor = commands(choice, current_location, current_floor)
    time.sleep(3)