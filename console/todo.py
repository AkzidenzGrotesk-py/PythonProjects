import os, sys, keyboard, msvcrt

class ListItem:
    def __init__(self, text, state = False):
        self.text = text
        self.state = state

    def generate(self, crossformat = 'x'):
        return f"[{crossformat if self.state else ' '}] \033[0m {self.text}"


class Dodo:
    def __init__(self, clear_type = "cls"):
        print("~ Initiating...")
        self.list = []
        self.active = True
        self.clear_type = 'cls' if os.name=='nt' else 'clear'
        self.settings = {
            "color" : "0f",
            "select_format" : "30;47",
            "move_up" : "w",
            "move_down" : "s",
            "add_new_item" : "d",
            "quit" : "q",
            "check_off" : "space",
            "delete_sel_item" : "backspace",
            "save" : "ctrl"
        }
        self.selected = 0
        print("* Initiated.")

    def error_start(self):
        self.ers = [
            "file does not exist",
            "cannot change terminal color"
        ]

    def error(self, er_id: int, loc: str):
        print(f"\033[31merror in {loc}: {self.ers[er_id]}.\033[0m")
        sys.exit()
    
    def check_arguments(self):
        if len(sys.argv) > 1:
            self.file = sys.argv[1]
        else: self.file = ""

    def sel_cur_up(self, e):
        if self.selected > 0: self.selected -= 1

    def sel_cur_down(self, e):
        if self.selected < len(self.list): self.selected += 1

    def check_off(self, e):
        if self.selected < len(self.list): 
            self.list[self.selected].state = not self.list[self.selected].state
            csel = self.list[self.selected]
            self.list.sort(key = lambda elem: int(elem.state))
            self.selected = self.list.index(csel)
            os.system(self.clear_type)

    def del_sel_item(self, e):
        if self.selected < len(self.list): 
            del self.list[self.selected]
            os.system(self.clear_type)

    def end_prog(self, e):
        self.active = False

    def activate_hooks(self):
        keyboard.on_press_key(self.settings["move_up"], self.sel_cur_up)
        keyboard.on_press_key(self.settings["move_down"], self.sel_cur_down)
        keyboard.on_press_key(self.settings["quit"], self.end_prog)
        keyboard.on_press_key(self.settings["check_off"], self.check_off)
        keyboard.on_press_key(self.settings["delete_sel_item"], self.del_sel_item)

    def start(self):
        # loading error system
        print(f"~ Loading error system...")
        self.error_start()
        print(f"* Error system loaded, continuing...")

        # reading arguments
        print("~ Checking arguments...")
        self.check_arguments()
        print(f"* Arguments read, continuing...")

        # loading file
        if self.file:
            print(f"~ Loading list file...")
            if os.path.exists(self.file):
                with open(self.file, "r") as saved_list:
                    for i in saved_list.readlines():
                        if i[0] == "*":
                            self.list.append(ListItem(i[1:].rstrip(), True))
                        else: self.list.append(ListItem(i.rstrip()))

                print(f"* Sucessfully loaded {self.file}, continuing...")

            else: self.error(0, "start() -> loading file")
        
        else: 
            self.file = "untitled.li"
            print(f"* No list file, continuing...")


        # loading settings
        print("~ Loading settings...")
        if os.path.exists("default.st"):
            with open("default.st", "r") as saved_settings:
                setin = saved_settings.readlines()

            for s in setin:
                nl = s.split(":")
                if len(nl) >= 2:
                    sset = nl[0].strip()
                    self.settings[sset] = nl[1].strip()

            print(f"* Sucessfully loaded settings, continuing...")

        else:
            print("~ Settings file nonexistant, creating and using default")

            gt = ""
            for s in self.settings:
                gt += f"{s}:{self.settings[s]}\n"

            with open("default.st", "w") as settings_file:
                settings_file.write(gt)

            print(f"* Sucessfully loaded settings, continuing...")

        # activating settings
        print("~ Activating settings...")
        if os.system(f"color {self.settings['color']}") == 1:
            self.error(1, "start() -> activating settings")

        self.activate_hooks()

        print(f"* Settings active, continuing...")

        # starting
        print(f"* Starting...")
        self.main()

    def main(self):
        os.system(self.clear_type)

        self.list.sort(key = lambda elem: int(elem.state))
        while self.active:
            print("\033[0;0H\033[?25l", end = '')
            os.system(f"title Dodo - {self.file}")

            # print to-dos
            out = f"\n"
            for c, l in enumerate(self.list):
                out += (f"\033[{self.settings['select_format']}m" if c == self.selected else "") + " " + l.generate() + "\n"
            out += (f"\033[{self.settings['select_format']}m" if len(self.list) == self.selected else "") + " [ ] \033[0m "
            print(out, end = '')

            # check if add new item
            if keyboard.is_pressed(self.settings["add_new_item"]):
                keyboard.unhook_all()
                while msvcrt.kbhit(): msvcrt.getch()
                if len(self.list) == self.selected:
                    ni = input("\033[?25h")
                    self.list.append(ListItem(ni))
                else:
                    ni = input(f"\033[?25h\033[{self.selected + 2}d\033[0K")
                    self.list[self.selected] = ListItem(ni, self.list[self.selected].state)
                self.activate_hooks()

            # save
            if keyboard.is_pressed(self.settings["save"]):
                if self.file == "untitled.li":
                    keyboard.unhook_all()
                    while msvcrt.kbhit(): msvcrt.getch()
                    self.file = input("\033[?25henter file name: ")
                    self.activate_hooks()

                txt = ""
                for i in self.list:
                    if i.state: txt += "*"
                    txt += i.text + "\n"
                with open(self.file, "w") as wfile:
                    wfile.write(txt)

                os.system(self.clear_type)

        print("\n")


        



def main():
    d = Dodo()
    d.start()

if __name__ == "__main__":
    main()
