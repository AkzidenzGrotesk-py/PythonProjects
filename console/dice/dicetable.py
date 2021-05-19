import sys, random

class DiceTable:
    def __init__(self, text):
        self.text = text
        self.dice = {
            "entry" : "",
            "custom" : [],
            "tables" : {}
        }
        self.cdicetable = ""
        self.cline = 0

        for j, t in enumerate(self.text):
            self.text[j] = t.strip()

        self.fill_dice_table()

    def error(self, text, etype = 0, fatal = False):
        if etype == 0: print(f"@ line {self.cline+1}: \033[31m" + text + "\033[0m")
        elif etype == 1: print(f"@ line {self.cline+1}: \033[33m" + text + "\033[0m")
        elif etype == 2: print(f"@ line {self.cline+1}: " + text)
        elif etype == 3: print(f"@ exec: " + text)

        if fatal: sys.exit()

    def fill_dice_table(self):
        for i, t in enumerate(self.text):
            self.cline = i
            tokens = t.split(" ")
            # print(tokens)
            try:
                if tokens[0] == "table":
                    if self.cdicetable != "":
                        self.error("Have not properly closed last table.", 2, True)
                    if tokens[1][0] == "d":
                        if tokens[1][1:].isnumeric():
                            if tokens[2][0] == '#':
                                self.dice["tables"][tokens[2][1:]] = ["" for i in range(int(tokens[1][1:]))]
                                self.cdicetable = tokens[2][1:]
                            else: self.error("Missing table ID operator.", 2, True)
                        else: self.error("Dice type not numeric.", 2, True)
                    else: self.error("Missing dice operator.", 2, True)
            
                elif tokens[0].isnumeric():
                    if len(self.dice["tables"][self.cdicetable]) < int(tokens[0]):
                        self.error("Overflowing dice table index, increase dice size.", 2, True)
                    self.dice["tables"][self.cdicetable][int(tokens[0])-1] = " ".join(tokens[1:])

                elif tokens[0] == "entry": self.dice["entry"] = tokens[1][1:]

                elif tokens[0] == "custom":
                    self.dice["custom"].append([[], []])
                    side = 0
                    for t in tokens[1:]:
                        if t == ":":
                            side = not side
                        else: self.dice["custom"][-1][side].append(t)
                        
                elif tokens[0] == "": continue

                elif tokens[0] == ".": self.cdicetable = ""

                else: self.error("Unrecognized token.", 2, True)
            except IndexError:
                self.error("Token overflow. Index non-functional.", 2, True)

        # print(self.dice)
        self.interpret_tables()

    def roll_in_current_table(self, table):
        x = random.randrange(len(table))
        s = table[x]
        if s[0] == "#":
            s = self.roll_in_current_table(self.dice["tables"][s[1:]])

        return s

    def interpret_tables(self):
        self.cdicetable = self.dice["entry"]

        while True:
            i = input("~$ ").lower().split(" ")

            try:
                for b, c in enumerate(self.dice["custom"]):
                    if c[0] == i:
                        i = c[1]
                        
                if i[0] == "roll":
                    if i[1].isnumeric():
                        for x in range(int(i[1])):
                            s = self.roll_in_current_table(self.dice["tables"][self.cdicetable])
                            print(s)
                    elif i[1][0] == "#":
                        if i[2] == None:
                            s = self.roll_in_current_table(self.dice["tables"][i[1][1:]])
                            print(s)
                        if i[2].isnumeric():
                            for x in range(int(i[2])):
                                s = self.roll_in_current_table(self.dice["tables"][i[1][1:]])
                                print(s)
                        else: self.error("Roll count not numeric.", 3, False)
                    else: self.error("Roll argument 2 is not valid.", 3, False)

                elif i[0] =="exit": sys.exit()

                else: self.error("Unrecognized command", 3, False)
            except IndexError:
                self.error("Input has wrong index of tokens.", 3, False)
                    


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        t = sys.argv[1]
        with open(t, "r") as file:    
            dt = DiceTable(file.readlines())
