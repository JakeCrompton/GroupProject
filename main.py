# If the script doesnt work (says the file doesnt exist or sum) type in "cd yourfilelocation" in the output
# means we can change stuff inside the map and it would work as it would as if it was something else (Data wise)

# importing json and os so it can find the files + pygame for the window
import json, os, pygame, sys

# loads the json map file
base_path = os.path.dirname(__file__)
mapFile = os.path.join(base_path, "mapLoader.json")

# reads the json file 
with open(mapFile, "r") as file:
    mapData = json.load(file)

pygame.init()
# pygame settings (for the window)
grid_size = 20
grid_width = 25  # how many squares on width
grid_length = 25  # how many squares on length
window_width = grid_size * grid_width
window_length = grid_size * grid_width

# colours (RGB)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# create woindow
screen = pygame.display.set_mode((window_width, window_length))
pygame.display.set_caption("Test grid")

# main loop (will mvoe after testing)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white) # doesnt work rn

    # grid lines
    for x in range(0, window_width, grid_size):
        pygame.draw.line(screen, black, (x, 0), (x, window_length))
    for y in range(0, window_length, grid_size):
        pygame.draw.line(screen, black, (0, y), (window_width, y))

    pygame.display.flip()

pygame.quit()
sys.exit()

# gets player data
player_location = mapData['player']['start_location']
inventory = mapData['player']['inventory']

print(f"You will start in {player_location}")
print(f"you have {inventory} in your inventory")

# get info about new room
current_room = mapData['Rooms'][player_location]
print(f"\n{current_room['description']}")
print(f"Items here: {current_room['items']}")
print(f"Exits: {list(current_room['exits'].keys())}")

print(f"Where would you like to go? {current_room['exits']}")
direction = input(">").strip().lower()

# check if the direction is valid
if direction in current_room['exits']:
    new_room = current_room['exits'][direction]
    player_location = new_room
    print(f"\nYou have moved {direction} to the {player_location}")
    if current_room["items"]:  # THIS WAS JUST TO TEST ADDING ITEMS (still not finished, adds the [''] to the item)
        inventory.insert(0, current_room["items"])
        print(f"Added {current_room['items']} to your inventory")
        print(f"This is your inventory now: {inventory}")  # FIX THIS 
else:
    print("You cannot move that way")