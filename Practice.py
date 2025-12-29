import json, os, sys, time
base_path = os.path.dirname(__file__) # finds the directory for the files
shopFile = os.path.join(base_path, "Stats.json")

with open(shopFile, "r") as file:
    shopData = json.load(file) 

balance = 200 #Just an example balance, these past lines aren't necessary for main.
def openShop(argument, mapData, current_location, current_floor):
    global player_stats  #this allows us to update player stats in this function

    print(f"Your balance is: {balance}") #would also have to create a balance variable
    print("Available Upgrades:")
    for idx, item in enumerate(shopData["stat_shop"]):
        print(f"{idx}.{item["name"]} - Cost: {item["cost"]} Bought: {item["times_bought"]}")


openShop(None, None, None, None)
