import json, os, sys, time
base_path = os.path.dirname(__file__) # finds the directory for the files
shopFile = os.path.join(base_path, "Stats.json")

with open(shopFile, "r") as file:
    shopData = json.load(file) 

balance = 200 #Just an example balance, these past lines aren't necessary for main.
def openShop(argument, mapData, current_location, current_floor):
    global player_stats  #this allows us to update player stats in this function
    global balance
    
    print(f"Your balance is: {balance}") #would also have to create a balance variable
    print("Available Upgrades:")
    for idx, item in enumerate(shopData["stat_shop"]):
        print(f"{idx}.{item["name"]} - Cost: {item["cost"]} Bought: {item["times_bought"]} Purpose: {item["id"]}")
    print("Enter the number of the upgrade to buy or -1 to exit")
    choice = input(">").strip()

    try:
        idx = int(choice)
        if idx == -1:
            print("Exiting Shop")
            return current_location
        elif 0 <= idx < len(shopData["stat_shop"]):
            item = shopData["stat_shop"][idx]
            cost = item["cost"]
            if balance >= cost: 
                balance = balance - cost
                print(f"New balance is {balance} ")
                item["times_bought"] +=1
                item["cost"] = int(item["cost"]) * 1.5
                print(f"You've bought {item["name"]}")
                print(f"New cost: {item["cost"]}, Times bought: {item["times_bought"]}")
            else:
                print(f"Not enough balance. Needed: {item["cost"]}, You have {balance}")
        else:
            print("Invalid number. Please choose a valid answer")
    except ValueError:
        print("Invalid input. Please enter a number")        
openShop(None, None, None, None)
