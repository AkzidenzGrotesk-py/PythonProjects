class ForgeFindReplace:
    def __init__(self):
        self.Forge = None

    def initiate(self):
        pass

    def open_loop(self):
        pass

    def close_loop(self):
        pass

    def commands(self, cmds, l_cmds):
        if cmds[0] == "/find":
            if l_cmds < 2: self.Forge.er("fr_0000")
            updt = []
            texttf = " ".join(cmds[1:])
            for l in self.Forge.content:
                updt.append(l.replace(texttf, "\033[43m" + texttf + "\033[0m"))

            self.Forge.clear_screen()
            self.Forge._format_top_line(f"0.      Forge :: {self.Forge.filename} - Highlighted: '{texttf}'")
            for c, lns in enumerate(updt):
                print("\033[0m" + str(c + 1) + ".\t" + lns)

            self.Forge.report(f"~ instances of '{texttf}'~")
            return True

        if cmds[0] == "/replace":
            if l_cmds < 3: self.Forge.er("fr_0001")
            texttr = cmds[1]
            texttrw = cmds[2]
            updt = []
            for l in self.Forge.content:
                updt.append(l.replace(texttr, texttrw))

            self.Forge.content = updt

            self.Forge.reload_display()
            self.Forge.report(f"~ instance of '{texttr}' -> '{texttrw}' ~")
            return True

        return False

    def reload(self):
        pass

    def extend_errors(self):
        return {
            "fr_0000" : "not enough keywords to find",
            "fr_0001" : "not enough keywords to replace"
        }
