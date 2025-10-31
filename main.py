# If the script doesnt work (says the file doesnt exist or sum) type in "cd yourfilelocation" in the output

import json, os

# Find the file location
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "mapLoader.json")

with open(file_path, "r") as file:
    data = json.load(file)

print(data)