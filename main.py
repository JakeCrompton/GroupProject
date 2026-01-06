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
    npc_file = json.load(file)
    npcData = npc_file["Main quest"]
    enemyData = npc_file["Enemies"]

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
        "talk": TalkTo,
        "shop": shop,
        "save": save_game,
    }    

    if command in actions: # checks that the command is valid
        return actions[command](arguement, mapData, current_location, current_floor) # this runs the function with the specified input
    else:
        print("Invalid input")
        return current_location, current_floor

def go(direction, mapData, current_location, current_floor):
    global player_inventory

    try:
        room_data = mapData[current_floor][current_location]
        exits = room_data.get('exits', {})

        if direction not in exits:
            print("Not a valid direction")
            return current_location, current_floor
        
        destination = exits[direction]

        if destination in mapData:
            new_floor = destination
            new_location = mapData[new_floor]['start_location']
            print(f"You move to the {new_floor} using {new_location}")
            return new_location, new_floor

        if destination in mapData[current_floor]:
            required_items = mapData[current_floor][destination].get('required_items', [])
            for item in required_items:
                if item not in player_inventory:
                    print(f"You cannot enter {destination} without {item}")
                    return current_location, current_floor
            
        new_location = destination
        new_floor = current_floor
        print(f"You move to {new_location}")

        room = mapData[current_floor][destination]
        min_enemies = room.get('minAmountOfEnemies', 0)
        max_enemies = room.get('maxAmountOfEnemies', 0)

        if max_enemies > 0:
            spawn_enemies(min_enemies, max_enemies)
        
        return new_location, new_floor
    
    except KeyError as e:  # Error handling incase the player goes to a different direction
        print("Movement error:", e)
        return current_location, current_floor

def inventory(argument, mapData, current_location, current_floor):
    while True:
        clearOutput()

        print("Equipped:")
        for slot, item in Equipped.items():
            print(f"-   {slot}: {item if item != 0 else 'None'}")

        if sum(player_inventory.values()) >= 5:
            print("\nYour inventory is full")

        if len(player_inventory) == 0:
            print("\nYou have nothing in your inventory")
            time.sleep(2)
            return current_location, current_floor
        
        print("\nYou currently have:")
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

            item_name_input = item_input.lower()
            matched_item = None
            for key in player_inventory:
                if key.lower() == item_name_input:
                    matched_item = key
                    break
            if not matched_item:
                print("You dont have that item")
                continue
            item_name = matched_item

            if item_name in itemsData['Weapons']:
                weapon = itemsData['Weapons'][item_name]
                slot = weapon['Slot']
                damage = weapon['Damage']

                old_weapon = Equipped.get(slot)

                if old_weapon and old_weapon != 0:
                    PlayerStats['WeaponDamage'] -= itemsData['Weapons'][old_weapon]['Damage']
                    player_inventory[old_weapon] = player_inventory.get(old_weapon, 0) + 1

                Equipped[slot] = item_name
                PlayerStats['WeaponDamage'] += damage

                player_inventory[item_name] -= 1
                if player_inventory[item_name] <= 0:
                    del player_inventory[item_name]

                print(f"You equipped {item_name} (+{damage} damage)")

            elif item_name in itemsData['Armour']:
                armour = itemsData['Armour'][item_name]
                slot = armour['Slot']
                defence = armour['Defence']
 
                old_item = Equipped.get(slot)
                if old_item and old_item != 0:
                    PlayerStats['Defence'] -= itemsData['Armour'][old_item]['Defence']

                Equipped[slot] = item_name
                PlayerStats['Defence'] += defence

                player_inventory[item_name] -= 1
                if player_inventory[item_name] <= 0:
                    del player_inventory[item_name]

                print(f"You equipped {item_name} in {slot} (+{defence} defence)")

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

    while True:
        print("What would you like to view?")

        for category in shopData['Shop']:
            print(f"- {category}")

        print("Type a category name or 'back'")
        purchase_option = input("> ").strip().title()

        if purchase_option.lower() in ("back", "go back"):
            return current_location, current_floor
        
        if purchase_option not in shopData['Shop']:
            print("Invalid category")
            continue

        category_items = shopData['Shop'][purchase_option]

        while True:
            clearOutput()
            print(f"{purchase_option} for sale:")

            if not category_items:
                print("Nothing left in stock")
                break

            for item, data in category_items.items():
                print(f"- {item} | {data['Price']} coins | Stock: {data['Quantity']}")

            print("Commands:")
            print("-    buy <item name>")
            print("-    back")

            shop_dialog = input("> ").strip()
            if not shop_dialog:
                print("Please enter a command")
                continue

            shopWords = shop_dialog.split()
            if shopWords[0].lower() == "back":
                break

            if shopWords[0].lower() == "buy":
                if len(shopWords) < 2:
                    print("Buy what?")
                    continue

                item_name_input = " ".join(shopWords[1:]).lower()
                matched_item = None
                for key in category_items:
                    if key.lower() == item_name_input:
                        matched_item = key
                        break

                if not matched_item:
                    print("Invalid item")
                    time.sleep(1)
                    continue

                item = category_items[matched_item]

                if item['Quantity'] <= 0:
                    print("That item is out of stock")
                    continue

                if PlayerInfo['Money'] < item['Price']:
                    print("You do not have enough money")
                    continue

                PlayerInfo['Money'] -= item['Price']
                player_inventory[matched_item] = player_inventory.get(matched_item, 0) + 1
                item['Quantity'] -= 1

                print(f"You bought {matched_item}")
                print(f"{matched_item} added to your inventory")
                time.sleep(1)

                if item['Quantity'] <= 0:
                    category_items.pop(matched_item)
                continue

            print("Invalid command")

def save_game(arugment, mapData, current_location, current_floor):
    save_data = {
        "PlayerInfo": PlayerInfo,
        "PlayerStats": PlayerStats,
        "PlayerSkills": PlayerSkills,
        "Equipped": Equipped,
        "Inventory": player_inventory,
        "Location": {
            "Floor": current_floor,
            "Location": current_location
        }
    }

    with open(saveFile, "w") as file:
        json.dump(save_data, file, indent = 4)

    print("Game saved successfully!")
    time.sleep(2)
    return current_location, current_floor

def load_save():
    global PlayerInfo, PlayerStats, PlayerSkills
    global Equipped, player_inventory
    global current_location, current_floor

    if not os.path.exists(saveFile):
        print("No save file found")
        return
    
    with open(saveFile, "r") as file:
        data = json.load(file)

    PlayerInfo.update(data['PlayerInfo'])
    PlayerStats.update(data['PlayerStats'])
    PlayerSkills.update(data['PlayerSkills'])
    Equipped.update(data['Equipped'])

    player_inventory.clear()
    player_inventory.update(data['Inventory'])

    current_floor = data['Location']['Floor']
    current_location = data['Location']['Location']

    print("Game loaded successfully")
    time.sleep(2)

def spawn_enemies(min_enemies, max_enemies):
    EnemyInRoom.clear() # clears the room every time it is called so it doesnt have previous data inside it

    amount = random.randint(min_enemies, max_enemies)

    for _ in range(amount):
        enemy = random.choice(enemyData).copy()
        EnemyInRoom.append(enemy)

    for enemy in EnemyInRoom:
        fight_enemy(enemy)

def fight_enemy(enemy):
    time.sleep(1)
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
                    damageDealt = (
                        PlayerSkills[chosen_skill.capitalize()] * PlayerStats['Strength']
                        + PlayerStats.get("WeaponDamage", 0)
                    )
                    enemy['Health'] -= damageDealt
                    print(f"You used {chosen_skill.capitalize()} and dealt {damageDealt} damage! The {enemy['Name']} has {enemy['Health']}hp remaining")

                    if enemy['Health'] <= 0:
                        print(f"The {enemy['Name']} has been defeated!")
                        enemyDefeated = True
                        PlayerInfo["Money"] += enemy['Cash']
                        print(f"You found {enemy['Cash']} coins on the {enemy['Name']}")
                        add_experience(enemy['XP'])
                        return current_location, current_floor

                enemy_damage = max(
                    0,
                    enemy['Damage'] - PlayerStats.get("Defence", 0)
                )
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
                    print("Game over!")
                    sys.exit()

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
                        PlayerInfo['Health'] = PlayerInfo['Max Health']
                        
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

def startGame():
    print("Would you like to start a New game or Continue?")
    NewOrLoad = input("> ").lower().strip()
    if NewOrLoad == "new game" or NewOrLoad == "new":
        print("Starting New game.")
        print("Remember typing 'help' will display all commands avaliable")
        time.sleep(1)
    elif NewOrLoad == "load save" or NewOrLoad == "continue":
        load_save()
    time.sleep(2)

def TalkTo(arugment, mapData, current_location, current_floor):
    room = mapData[current_floor][current_location]
    npc_name = room.get("NPC")

    if not npc_name:
        print("There is no one here to talk to")
        time.sleep(2)
        return current_location, current_floor
    
    npc = npcData.get(npc_name)
    if not npc:
        print("This person doesnt respond")
        time.sleep(2)
        return current_location, current_floor
    
    print(f"You talk to {npc_name}...")
    time.sleep(1)

    requirements = npc.get("Requirements")
    voiceline = npc.get("Voiceline", "...")

    if requirements == "None":
        print(f"{npc_name}: {voiceline}")
        time.sleep(3)
        return current_location, current_floor
    
    if isinstance(requirements, int):
        if PlayerInfo['Level'] >= requirements:
            print(f"{npc_name}: {voiceline}")
        else:
            print(f"{npc_name}: Come back to me when your ready.")
            print(f"(Requires level {requirements})")
        time.sleep(3)
        return current_location, current_floor
    
    if isinstance(requirements, list):
        missing = []

        for req in requirements:
            if req not in player_inventory:
                missing.append(req)

        if missing:
            print(f"{npc_name}: Come back to me when your ready.")
            print("Missing:")
            for m in missing:
                print(f"- {m}")
        else:
            print(f"{npc_name}: {voiceline}")

        time.sleep(3)
        return current_location, current_floor

def add_experience(amount):
    PlayerInfo["Experience"] += amount
    print(f"You have gained {amount}xp!")

    while PlayerInfo["Experience"] >= xp_to_lvlup(PlayerInfo["Level"]):
        PlayerInfo["Experience"] -= xp_to_lvlup(PlayerInfo["Level"])
        PlayerInfo["Level"] += 1
        PlayerInfo['Max Health'] += 10
        PlayerInfo["Stat Points"] += 1
        PlayerInfo["Health"] = PlayerInfo["Max Health"]

        print(f"Level up! You are now level {PlayerInfo['Level']}!")
        print(f"You have {PlayerInfo['Stat Points']} unspent skill points.")

    print(
        f"Level {PlayerInfo['Level']} "
        f"{PlayerInfo['Experience']}xp/{xp_to_lvlup(PlayerInfo['Level'])}xp")
    
    if PlayerInfo['Stat Points'] > 0:
        spend_skill_point()

    return current_location, current_floor

def xp_to_lvlup(level):
    return 100 * (level + 1) # can change the amount of xp needed by changing the values (100 xp per level)

def spend_skill_point():
    print(f"What would you like to put your skill points into?")
    for ind in PlayerStats.items():
        print(f"-   {ind}")
    spendSkillPoint = input("> ").lower().strip()
    if spendSkillPoint.capitalize() in PlayerStats:
        PlayerStats[spendSkillPoint.capitalize()] += 1
        print(f"You have increased your {spendSkillPoint} by 1!")
        if spendSkillPoint == "health":
            PlayerInfo['Max Health'] += 20
            PlayerInfo['Health'] += 20
    else:
        print("Invalid input")
    time.sleep(5)
    return current_location, current_floor

def check_win_condition(current_location, inventory):
    if current_location == "Main door" and "Main door key" in inventory:
        print("You unlocked the door and escaped!")
        print("You win!")
        return True
    return False

clearOutput()
startGame()
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
        print("\nItems in room:")
        for items in mapData[current_floor][current_location]['items']:
            print(f"-   {items.capitalize()}")

    npc_name = mapData[current_floor][current_location].get("NPC")
    if npc_name:
        print(f"\nYou see {npc_name} here")
        print(f"You can talk to them using 'talk'")

    print("\nWhat would you like to do?")
    choice = input("> ").lower().strip()
    current_location, current_floor = commands(choice, current_location, current_floor)
    if check_win_condition(current_location, player_inventory):
        break
    time.sleep(3)