# If the script doesnt work (says the file doesnt exist or sum) type in "cd yourfilelocation" in the output
# means we can change stuff inside the map and it would work as it would as if it was something else (Data wise)

import json, os

# Find the file location
base_path = os.path.dirname(__file__)
mapFile = os.path.join(base_path, "mapLoader.json")

# opens the json file
with open(mapFile, "r") as file:
    mapData = json.load(file)


print(f"The map data: {mapData}")
