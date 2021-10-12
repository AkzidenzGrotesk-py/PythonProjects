class ForgeHighlightMarkdown:
    def __init__(self):
        self.Forge = None

    def initiate(self):
        self.colours = {
            "highlight_hash" : "33",
            "link" : "94;4"
        }
        self.enable_highlighting = True

    def open_loop(self):
        pass

    def close_loop(self):
        pass

    def commands(self, cmds, l_cmds):
        if cmds[0] == "/tglhl":
            self.enable_highlighting = not self.enable_highlighting
            self.Forge.reload_display()
            self.Forge.report("$ markdown highlighting toggled $")
            return True
        return False

    def reload(self):
        self.Forge.clear_screen()
        self.Forge.top_line()
        if not self.enable_highlighting:
            for c, lns in enumerate(self.Forge.content):
                print("\033[0m" + str(c + 1) + ".\t" + lns)
            return

        else:
            for c, lns in enumerate(self.Forge.content):
                colour = 0
                if len(lns) > 0:
                    if lns[0] == "#": colour = self.colours["highlight_hash"]
                    if len(lns) > 4:
                        if lns[:5] == "https": colour = self.colours["link"]

                print("\033[0m" + str(c + 1) + ".\t" + f"\033[{colour}m" + lns + "\033[0m")

    def extend_errors(self):
        return {}
