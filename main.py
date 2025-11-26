import json, os, pygame, sys, time

base_path = os.path.dirname(__file__) # finds the directory for the files
mapFile = os.path.join(base_path, "mapLoader.json")

with open(mapFile, "r") as file:
    mapData = json.load(file) # loads the json file as a variable

# Functions
def clearOutput(): # call this function when you want to clear whatever is in the output (cleans it up)
    os.system('cls')

