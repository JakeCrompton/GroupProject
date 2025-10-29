# If the script doesnt work (says the file doesnt exist or sum) type in "cd yourfilelocation" in the output

import json

with open("mapLoader.json", "r") as file:
    data = json.load(file)

print(data)