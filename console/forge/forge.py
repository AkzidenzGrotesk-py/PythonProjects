import os, sys, copy, forge_ext


class Forge:
    def __init__(self):
        self.line = 1
        self.tabs = ""
        self.content = []
        self.filename = "untitled.txt"
        self.active = True
        self.add_type = "reset"

    # START/QUIT
    def start(self):
        self.init_ext()
        self.init_er()
        self.loop()

    def inactivate(self):
        self.active = False

    def quit(self):
        self.inactivate()
        sys.exit()

    # PACKAGES
    def init_ext(self):
        self.extension = forge_ext.ForgeExtensionHandler(self)
        self.extension.initiate()

    # ERROR HANDLING
    def init_er(self):
        self.errors = {
            # 0: execution errors
            # 1: command errors
            "1_0000" : ["no line to jump to", False],
            "1_0001" : ["invalid line number", False],
            "1_0002" : ["no line to delete", False],
            "1_0003" : ["no name to set to", False],
            "1_0004" : ["no line to add", False],
            "1_0005" : ["no commands to execute", False],
            "1_0006" : ["no mode to switch to", False],
            # 2: file handling
            "2_0000" : ["file does not exist", False]
        }
        self.errors = self.errors | self.extension.extend_errors()

    def er(self, id):
        print(f"\033[31merror ({id}): {self.errors[id][0]}.\033[0m")
        if self.errors[id][1]: self.quit()

    # UTILITY
    def set_title(self):
        self._set_title(f"Forge - {self.filename}")

    def _set_title(self, title):
        os.system(f"title {title}")

    def top_line(self):
        self._format_top_line(f"0.      Forge :: {self.filename} -")

    def _format_top_line(self, text):
        print(f"\033[30;47m{text}\033[0m")

    def clear_screen(self):
        os.system("cls")

    def reload_display(self):
        self.clear_screen()
        self.top_line()
        for c, lns in enumerate(self.content):
            print("\033[0m" + str(c + 1) + ".\t" + lns)

        self.extension.reload()

    def report(self, msg):
        print(f" .\t\033[33m{msg}\033[0m")

    def jump_to_line(self, cmds, l_cmds):
        if not l_cmds > 1:
            self.er("1_0000")
            return
        if not cmds[1].isdigit:
            self.er("1_0001")
            return
        line_to_jump = int(cmds[1])
        if line_to_jump > len(self.content) + 1 or int(cmds[1]) < 1:
            self.er("1_0001")
            return

        self.line = line_to_jump
        self.report(f"^ {cmds[1]} ^")

    def del_line(self, cmds, l_cmds):
        if not l_cmds > 1:
            self.er("1_0002")
            return
        if not cmds[1].isdigit:
            self.er("1_0001")
            return
        line_to_del = int(cmds[1])
        if line_to_del > len(self.content) + 1 or int(cmds[1]) < 1:
            self.er("1_0001")
            return

        self.report(f"~ {cmds[1]} ~")
        del self.content[line_to_del - 1]
        self.line -= 1

    def add_line(self, cmds, l_cmds):
        if not l_cmds > 1:
            self.er("1_0004")
            return
        if not cmds[1].isdigit:
            self.er("1_0001")
            return

        line_to_add = int(cmds[1])
        if line_to_add > len(self.content) + 1 or int(cmds[1]) < 1:
            self.er("1_0001")
            return

        self.report(f"+ {cmds[1]} +")
        self.content.insert(line_to_add - 1, "")
        self.line += 1

    def run_command(self, cmds, l_cmds):
        if not l_cmds > 1:
            self.er("1_0005")
            return

        tcmd = " ".join(cmds[1:])
        self.report(f"/ {tcmd} /")
        os.system(tcmd)

    def set_name(self, cmds, l_cmds):
        if not l_cmds > 1:
            self.er("1_0003")
            return

        nname = " ".join(cmds[1:])
        self.report(f"_ {nname} _")
        self.filename = nname

    def save_file(self, cmds, l_cmds):
        if l_cmds > 1:
            self.filename = " ".join(cmds[1:])

        with open("files/" + self.filename, "w") as ftw:
            ftw.write("\n".join(self.content))

        self.report(f"< {self.filename} <")

    def open_file(self, cmds, l_cmds):
        if l_cmds == 1:
            if not os.path.exists("files/" + self.filename):
                self.er("2_0000")
                return

        else:
            if not os.path.exists("files/" + " ".join(cmds[1:])):
                self.er("2_0000")
                return
            self.filename = " ".join(cmds[1:])


        with open("files/" + self.filename, "r") as ftr:
            cont = ftr.readlines()
            self.content = [dl.rstrip("\n") for dl in cont]
            self.line = len(cont) + 1
            self.tabs = ""

            for j in cont[-1]:
                if j == "\t":
                    self.tabs += "\t"
                else: break

        self.reload_display()
        self.report(f"> {self.filename} >")

    def cls_content(self):
        confirm = input("\t\033[33m(y/n) \033[0m")
        if confirm[0] == "y":
            self.content = []
            self.tabs = ""
            self.line = 1
        else:
            return

        self.reload_display()
        self.report(f"~ ~ ~")

    def change_mode(self, cmds, l_cmds):
        if not l_cmds > 1:
            self.er("1_0006")
            return

        if cmds[1] in ["-r", "-reset"]:
            self.add_type = "reset"
            self.report(f"| reset |")
        elif cmds[1] in ["-ae", "-add_end"]:
            self.add_type = "add_end"
            self.report(f"| add to end |")
        elif cmds[1] in ["-as", "-add_start"]:
            self.add_type = "add_start"
            self.report(f"| add to start |")

    # MAIN
    def handle_commands(self, raw):
        cmds = raw.split(" ")
        l_cmds = len(cmds)

        if cmds[0] in ["/exit", "/quit"]:
            self.inactivate()
            return True

        elif cmds[0] in ["/r", "/reload"]:
            self.reload_display()
            return True

        elif cmds[0] in ["/j", "/jump"]:
            self.jump_to_line(cmds, l_cmds)
            return True

        elif cmds[0] in ["/d", "/del"]:
            self.del_line(cmds, l_cmds)
            return True

        elif cmds[0] in ["/n", "/name"]:
            self.set_name(cmds, l_cmds)
            return True

        elif cmds[0] in ["/s", "/save"]:
            self.save_file(cmds, l_cmds)
            return True

        elif cmds[0] in ["/o", "/open"]:
            self.open_file(cmds, l_cmds)
            return True

        elif cmds[0] in ["/c", "/clear"]:
            self.cls_content()
            return True

        elif cmds[0] in ["/a", "/add"]:
            self.add_line(cmds, l_cmds)
            return True

        elif cmds[0] in ["/b", "/bash"]:
            self.run_command(cmds, l_cmds)
            return True

        elif cmds[0] in ["/m", "/mode"]:
            self.change_mode(cmds, l_cmds)
            return True

        elif cmds[0] in ["/h", "/help"]:
            self.filename = "using_forge.md"
            self.open_file("/o using_forge.md", 1)
            return True

        elif cmds[0] == "/": return True

        if self.extension.commands(cmds, l_cmds):
            return True

        return False

    def collect_tabs(self, inp):
        for j in inp:
            if j == "\t":
                self.tabs += "\t"
                inp = inp[1:]
            if j == ".":
                self.tabs = self.tabs[:-1]
                inp = inp[1:]
            else: break

        return inp

    def append_text(self, inp):
        if self.line > len(self.content):
            self.content.append(self.tabs + inp)
            return

        if self.add_type == "reset":
            self.content[self.line - 1] = self.tabs + inp

        elif self.add_type == "add_end":
            self.content[self.line - 1] += self.tabs + inp

        elif self.add_type == "add_start":
            self.content[self.line - 1] = self.tabs + inp + self.content[self.line - 1]

    def loop(self):
        self.top_line()

        while self.active:
            self.set_title()
            self.extension.open_loop()

            inp = input(str(self.line) + ".\t" + self.tabs)
            inp = self.collect_tabs(inp)
            if self.handle_commands(inp): continue

            self.extension.close_loop()
            self.append_text(inp)
            self.line += 1

        self.quit()




def main():
    f = Forge()
    f.start()


if __name__ == "__main__":
    main()
