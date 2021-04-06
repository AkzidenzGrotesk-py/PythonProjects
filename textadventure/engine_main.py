import sys

### GAME ENGINE FOR TEXT ADVENTURES
# ALPHA v0.2

# Game to import
from game_data import *
# ^^^ Link file in format ^^^

# designed by: akzidenz

def clr():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

def ln(x):
    if x == 0:
        print(line)
        pass
    if x == 1:
        return line
    else:
        return "Values 0 or 1"

line = "\n-----------------------------------------------------------------------\n"


### SYSTEM

# Has item system
def has_item(item):
    # Check inventory for item
    if inventory.get(item) != 0:
        return True
    else:
        return False
    
# Print corresponding room descriptions
def get_room():
    global current_room, room_descriptions, inventory, chest_state

    # Get room and print everything under "default"
    get_rooms = room_descriptions.get(current_room)
    print(get_rooms.get("default"))

    # Check for additional messages
    custom_room_additional_msgs(get_rooms, current_room)

# Using inventory objects to interact with others
def use_item(obj):
    global current_room, room_uses, room_messages, inventory
    for room in room_uses:
        if room == current_room:
            new = room_uses.get(room)
            for item in new:
                if item == obj:
                    print(room_messages.get(room).get(room_uses.get(room).get(obj)))

                    custom_uses(current_room, obj)
                    get_user_input()
    print(room_messages.get(0).get("error_cannot_use"))
    get_user_input()
    

# Pickup object system
def pickup(obj):
    global current_room, room_items, inventory
    # Check which items are in which rooms
    for room in room_items:
        # Check for current room
        if room == current_room:
            # If that item ("obj") can be pickup/exists in that room, pick it up, else; error
            check_for_items = room_items.get(room)
            for item in check_for_items:
                item_count = inventory.get(check_for_items.get(obj))
                if item == obj and item_count == 0:
                    # Prints and gives item
                    print(room_messages.get(room).get(room_items.get(room).get(item.replace(" ", "-") + "_MSG")))
                    inventory[room_items.get(room).get(item)] += 1
                    get_user_input()
                else:
                    print(room_messages.get(0).get("no_item_error"))
                        
                    get_user_input()
    print(room_messages.get(0).get("no_item_error"))
    get_user_input()


# Search rooms
def search():
    global current_room, room_items
    # Check which items are in which rooms
    for room in room_items:
        # Check for current room
        if room == current_room:
            # If there is an item that can be pickedup/exists in that room, pick it up, else; error
            check_for_items = room_items.get(room)
            for item in check_for_items:
                item_count = inventory.get(check_for_items.get(item))
                if item_count == 0:
                    # Prints and gives item
                    print(room_messages.get(room).get(room_items.get(room).get(item.replace(" ", "-") + "_MSG")))
                    inventory[room_items.get(room).get(item)] += 1
                    get_user_input()
                else:
                    print(room_messages.get(0).get("error_no_item"))
                        
                    get_user_input()
    print(room_messages.get(0).get("error_no_item"))
                        
    get_user_input()


# Movement inbetween rooms
def navigate_rooms(direction):
    global room_exits, current_room, room_messages

    # Get possible rooms
    for ways in room_exits:
        # Match with current room
        if ways == current_room:
            new_ways = room_exits.get(ways)
            # Get possible directions
            for dirct in new_ways:
                # Match with direction
                if direction == dirct:
                    # Update room
                    going_in_dirct = new_ways.get(dirct)

                    current_room = custom_room_entry_req(going_in_dirct, current_room)
                        
                    get_user_input()
                # Not a direction
                else:
                    error_msg = room_messages.get(0).get("cannot_go_that_way")

    print(error_msg)
    get_user_input()

# Print out inventory
def view_inventory():
    global inventory, line,ln
    to_output = ""
    item_count = 0
    for item in inventory:
        if inventory.get(item) != 0:
            to_output += item + " : " + str(inventory.get(item)) + "\n"
            item_count += 1
        else:
            continue
    ln(0)
    print("> Inventory [" + str(item_count) + "] :\n" + to_output + ln(1))
    get_user_input()

# check for input
def get_user_input():
    global inventory, room_items, line, ln, clr

    # Print room text and ask for input
    get_room()
    action = input(">>> ").lower().split(" ")
    ln(0)
    clr()
    
    # Check for cmd
    try:
        if action[0] == "exit" or action[0] == "quit":
            sys.exit()
        if action[0] == "debug":
            print(inventory)
            print(room_items)
            get_user_input()
        if action[0] == "inv" or action[0] == "inventory" or action[0] == "items":
            view_inventory()
        if action[0] == "search":
            search()
        if action[0] == "pickup" or action[0] == "grab":
            pickup(action[1].capitalize())
        if action[0] == "use":
            use_item(action[1].capitalize())
        elif action[0] == "move" or action[0] == "go":
            navigate_rooms(action[1])
        else:
            print(room_messages.get(0).get("not_cmd"))
            get_user_input()
    except:
        print(room_messages.get(0).get("not_cmd"))
        get_user_input()
        
def __run():
    clr()
    get_user_input()

__run()
    
