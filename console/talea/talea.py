import random, sys, re

class Talea:
    def __init__(self, text):
        self.unclean_text = text
        self.gen = {
            "fields" : {},
            "tables" : {},
            "conds" : {}
        }

        self.clean_text()
        self.convert_to_json()

    def clean_text(self):
        self.text = []

        for i, t in enumerate(self.unclean_text):
            if t != "" and t != "\n":
                self.text.append(t.replace("\t", "").strip())

    def convert_to_json(self):
        current_table = None
        current_condition = None
        for line in self.text:
            tok = line.split(" ")

            if tok[0] == "field":
                self.gen["fields"][tok[1]] = tok[2:]

            if tok[0] == "table":
                self.gen["tables"][tok[1]] = {
                    "dice" : tok[2],
                    "results" : {}
                }
                current_table = tok[1]
                current_condition = None

            if tok[0] == "?":
                if not tok[1] in self.gen["conds"]: self.gen["conds"][tok[1]] = {}
                self.gen["conds"][tok[1]][tok[2]] = []
                current_condition = [tok[1], tok[2]]
                current_table = None

            if tok[0] == ".":
                if current_table != None:
                    self.gen["tables"][current_table]["results"][tok[1]] = " ".join(tok[2:])

                if current_condition != None:
                    self.gen["conds"][current_condition[0]][current_condition[1]].append(" ".join(tok[1:]))

                # else: print("error.")

            #print(tok)

        #print()
        # print(self.gen)

    def replace_dice_format(self, txt):
        def roll_dice(ttxt):
            out = 0
            ttxt = ttxt.split("d")
            count = int(ttxt[0]); dice = int(ttxt[1]);

            for i in range(count):
                out += random.randrange(1, dice+1)

            return out

        dicesequences = re.compile("\[[0-9d\+\*-/\s]*\]").findall(txt)

        for s in dicesequences:
            dices = re.compile("\d+d\d+").findall(s)
            ns = s.replace("[","").replace("]","")
            for d in dices:
                ns = ns.replace(d, str(roll_dice(d)))

            txt = txt.replace(s, str(eval(ns)))

        return txt

    def deal_with_command(self, text):
        raw = text.split(":")
        for j, r in enumerate(raw):
            raw[j] = r.strip()

        if raw[0] == "print":
            print(self.replace_dice_format("".join(raw[1:])))

        if raw[0] == "roll":
            self.roll_on_table("".join(raw[1:]))

    def roll_on_table(self, table):
        t = self.gen["tables"][table]
        roll = self.replace_dice_format(t["dice"])
        for r in t["results"]:
            compile = r.split("-")
            if len(compile) == 2:
                if int(compile[0]) < int(roll) and int(compile[1]) > int(roll):
                    self.deal_with_command(t["results"][r])
            else:
                if int(compile[0]) == roll:
                    self.deal_with_command(t["results"][r])

    def run(self):
        # generate field choices
        fields = {}
        for f in self.gen["fields"]: fields[f] = ""
        for f in fields:
            c = ", ".join(self.gen["fields"][f])
            fields[f] = input(f"{f} ({c}): ")

        # do stuff
        for c in self.gen["conds"]:
            for c2 in self.gen["conds"][c]:
                if fields[c] == c2:
                    for a in self.gen["conds"][c][c2]:
                        self.deal_with_command(a)
                        #print(self.gen["conds"][c][c2])

        #print(fields)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as file:
            t = Talea(file.readlines())
        t.run()
