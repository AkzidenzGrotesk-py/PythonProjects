import copy

class ForgeHighlighter:
    def __init__(self):
        self.Forge = None

    def initiate(self):
        self.python_theme = {
            "keywords" : ["False", "await", "else", "import", "pass", "None", "break", "except", "in", "raise", "True", "class", "finally", "is", "return", "and", "continue", "for", "lambda", "try", "as", "def", "from", "nonlocal", "while", "assert", "del", "global", "not", "with", "async", "elif", "if", "or", "yield"],
            "keywords_c" : ["replace", "31"]
        }
        self.highlight_type = self.python_theme
        self.highlight = True

    def open_loop(self):
        pass

    def close_loop(self):
        pass

    def commands(self, cmds, l_cmds):
        if cmds[0] == "/hlt":
            if l_cmds < 2: self.Forge.er()
            if cmds[1] in ["python", "py", "python3"]:
                self.highlight_type = self.python_theme
            else:
                self.Forge.er("hl_0002")
                return True

            self.Forge.report(f"$ highlighting set to [{cmds[1]}] $")

            return True

        if cmds[0] == "/dhlt":
            self.highlight = not self.highlight
            self.Forge.reload_display()
            self.Forge.report("$ highlighting toggled $")
            return True

        return False

    def reload(self):
        self.Forge.clear_screen()
        self.Forge.top_line()

        if self.highlight:
            for c, lns in enumerate(self.Forge.content):
                print("\033[0m" + str(c + 1) + ".\t" + lns)
            return

        else:
            newforge = copy.copy(self.Forge.content)
            for h in self.highlight_type:
                if h[-2:] == "_c":
                    if self.highlight_type[h][0] == "replace":
                        for o in self.highlight_type[h[:-2]]:
                            for c, lns in enumerate(newforge):
                                newforge[c] = lns.replace(o, f"\033[{self.highlight_type[h][1]}m{o}\033[0m")

                                print("\033[0m" + str(c + 1) + ".\t" + lns)

            return


    def extend_errors(self):
        return {
            "hl_0001" : ["no highlighting language", False],
            "hl_0002" : ["unrecognized highlight type", False]
        }
