### GAME DATA
# THIS IS WHAT ENGINE_MAIN PARSES
# designed by: akzidenz


# DATA FOR DUNGEON/TEMPLATE

# Room ID: Specifiers/Titles
rooms = {
            0:"Main Menu",
            1:"Dungeon Entrance",
            2:"Dungeon First Room",
            3:"Dungeon Second Room",
            4:"Dungeon Third Room",
            5:"Dungeon Fourth Room"
        }

# Room Exits: Transport/Ways to move inbetween
room_exits = {
            0:{"start":1},
            1:{"south":2},
            2:{"north":1,"south":4,"east":3},
            3:{"west":2,"south":5},
            4:{"north":2,"east":5},
            5:{"north":3,"west":4}
        }

# Room Desc.: Messages that popup when you enter a room.
room_descriptions = {
            0:{
                "default":"Text Adventure Template, designed by: Kaz.\nYou commands such as ~move~/~go~,~pickup~/~grab~, ~search~ and ~use~, to explore this basic dungeon.\n----Examples: 'use key', 'move north', 'search', 'pickup apple', 'go east', etc. \nType GO START to begin."
            },
            1:{
                "default":"You are standing infront of a dark cave going downwards. \nThis entrance is to your south.",
                "has_not_gotten_torch":"\nYou see a torch near you, maybe you could light your way!"
            },
            2:{
                "default":"The cave is intresting, with vines and odd plants growing on the sides. \nYou see two other rooms to the south and east, \nand the light of the exit behind you (to the north).\nYou cannot see into the other rooms."
            },
            3:{
                "default":"The room is the same as the last,\nBehind you to the west is the original room and to the south is another room.\nNothing else seems to be there, but you faintly hear a stream.",
                "has_not_gotten_key":"\nWait, you also see a faint gleam of an oddly shaped piece of *metal*, maybe you should take it."
            },
            4:{
                "default":"This room is slightly different, but you see a locked chest infront of you. \nYou also hear the slight splashes of a stream.\nTo the north is the original room, and to the east is another room.",
                "fully_locked_chest":"\nThe chest is locked and has a chain that could be broken around it.",
                "half_unlocked":"\nOn the floor is a chain that you broke, and the chest still is locked"
            },
            5:{
                "default":"It seems this room is the source of the stream,\nAnother room is to the north and the west.\nIt's hard to see in the dark, it seems like there is something stopping the light of your torch from spreading.",
                "has_not_gotten_crowbar":"\nNothing major seems to be hiding, but maybe you could ~search~ the room."
            } 
        }


# Room Msgs: Messages that popup when an action is done or errors.
room_messages = {
            0:{
                "end":"> Thanks for playing, this is a template of what you can do with 'Text Adventure'! (To tell stories!)\n",
                "cannot_go_that_way":"> You can't do that!\n",
                "not_cmd":"> Not a valid command, try: ~move~/~go~,~pickup~/~grab~, ~search~, ~inv~/~items~/~inventory~ and ~use~ or to quit: ~quit~/~exit~\n",
                "no_item_error":"> Where is that?! (That item cannot be picked up, or does not exist.)\n",
                "error_no_item":"> There is nothing else to find! (That item cannot be picked up, or does not exist.)\n",
                "error_cannot_use":"> You cannot use that or you have nothing to do that with!\n"
            },
            1:{
                "too_dark":"> The cave is too dark, pickup the torch!\n",
                "torch_pickup":"> You picked up the torch! Now you can light your way. \n['Torch' added to inventory.]\n"
            },
            2:{
                "easter_egg":"> Oh, hello! I'm David the bug! I like the dark cave, you have fun, be careful! Here take this! \n['David's Charm' added to inventory.]\n"
            },
            3:{
                "key_pickup":"> You picked up the piece of metal, you realize it is covered in a green patina and is shaped like a key. \nIt is probably an old copper key. \n['Copper Key' added to inventory]\n"
            },
            4:{
                "pull_off_chain":"> You hack of the chain with some swift and strong movements, the chain breaks off with a metallic crack and hits the floor, echoing a loud smash as it hits the floor.\n",
                "static":"",
                "no_chain":"> There is no chain to pull off!\n",
                "still_chain":"> You can't unlock the chest, the chain is in the way.\n",
                "unlock_chest":"> You slowly unlock the chest, as it opens you see the fog in the cave darkens, and your torch fades into darkness. You hear a high pitched screech of some monster...\nMaybe you could have done something to stop its escape, and claim its treasure.\n",
                "has_charm_unlock":"> As you open the chest, the fog thickens and your torch goes out, you hear a screech of some monster...\nBut, you see a blinding flash of light as David's Charms pierces the darkness, the monster, a hideous bat with four heads, covers its eyes with its wings, as it slowly dissapates into nothingness. The chest glows bright with many treasure of riches unimaginable.\n"
            },
            5:{
                "crowbar_pickup":"> You find a crowbar in the water, very old, but not rusty. ['Crowbar' added to inventory.]\n"
            }
        }

# Inventory
inventory = {"Torch":0,"Crowbar":1,"Copper key":1,"David's Charm":0}

# Room Items: Items in certain rooms
room_items = {
            0:{},
            1:{"Torch":"Torch","Torch_MSG":"torch_pickup"},
            2:{"David's Charm":"David's Charm","David's-Charm_MSG":"easter_egg"},
            3:{"Metal":"Copper key","Metal_MSG":"key_pickup"},
            4:{},
            5:{"Crowbar":"Crowbar","Crowbar_MSG":"crowbar_pickup"}
        }

# Items usable in which rooms
room_uses = {
            0:{},
            1:{},
            2:{},
            3:{},
            4:{"Crowbar":"pull_off_chain","Copper-key":"static"},
            5:{}
        }

chest_state = 0 # 0:locked, 1:chain removed, 2:unlocked
current_room = 4


# CUSTOMIZE
### Do not remove or leave empty

def custom_room_entry_req(new_dir, new_current_room):
    import engine_main
    global current_room, room_descriptions, chest_state, room_messages

    if new_current_room != 1 or new_current_room == 1 and engine_main.has_item("Torch"):
        new_current_room = new_dir
        return new_current_room
    else:
        print(room_messages.get(1).get("too_dark") + "\n")
        return new_current_room
    

def custom_room_additional_msgs(c_room_data, new_current_room):
    import engine_main
    global current_room, room_descriptions, chest_state
    
    # print("Getting further")
    # print("CR: ", new_current_room)
    if new_current_room == 1 and not engine_main.has_item("Torch"):
        print(c_room_data.get("has_not_gotten_torch"))

    if new_current_room == 3 and not engine_main.has_item("Copper key"):
        print(c_room_data.get("has_not_gotten_key"))

    if new_current_room == 4 and chest_state == 0:
        print(c_room_data.get("fully_locked_chest"))

    if new_current_room == 4 and chest_state == 1:
        print(c_room_data.get("half_unlocked"))

    if new_current_room == 5 and not engine_main.has_item("Crowbar"):
        print(c_room_data.get("has_not_gotten_crowbar"))

    else:
        pass 
        # print("Failed.")

def custom_uses(new_current_room, used_item):
    import engine_main, sys
    global chest_state
    if used_item == "Crowbar" and chest_state == 0:
        chest_state = 1
    elif used_item == "Crowbar" and chest_state != 0:
        print(room_messages.get(4).get("no_chain"))

    if used_item == "Copper-key" and chest_state == 1 and engine_main.has_item("David's Charm"):
        print(room_messages.get(4).get("has_charm_unlock"))
        print("!!!!ENDING 2 COMPLETE!!!!")
        print("Good job! This is the good ending!")
        sys.exit()
        
    if used_item == "Copper-key" and chest_state == 1:
        chest_state = 2
        print(room_messages.get(4).get("unlock_chest"))
        print("!!!!ENDING 1 COMPLETE!!!!")
        print("Good job!")
        sys.exit()
    elif used_item == "Copper-key" and chest_state != 1:
        print(room_messages.get(4).get("still_chain"))
        
        
    
