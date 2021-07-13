from random import choice
from sys import argv
from pprint import pprint

class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.cchar = ""

    def advance(self):
        self.pos += 1
        if (self.pos) >= len(self.text):
            self.cchar = None
        else:
            self.cchar = self.text[self.pos]

    def back(self):
        self.pos -= 1
        if self.pos > 0:
            self.pos = 0
        self.cchar = self.text[self.pos]

    def peek(self):
        if self.pos > len(self.text):
            return None
        return self.text[self.pos+1]

    def whitespace(self):
        while self.cchar in [" ", "\n", "\t"] and not self.cchar == None:
            self.advance()

    def collect_alpha(self):
        a = ""

        while self.cchar.isalnum() or self.cchar in ["_","-"] and not self.cchar == None:
            a += self.cchar
            self.advance()

        # self.back()
        return a

    def collect_str(self, i):
        a = ""
        self.advance()

        while self.cchar != i and not self.cchar == None:
            a += self.cchar
            self.advance()

        # self.back()
        return a

    def next(self):
        self.advance()

        self.whitespace()
        if self.cchar == None: return ["END", None]
        if self.cchar.isalnum(): return ["TOK", self.collect_alpha()]
        if self.cchar in ["\"", "\'"]: return ["STR", self.collect_str(self.cchar)]

        if self.cchar == "*": return ["AST", "*"]
        if self.cchar == ",": return ["COM", ","]
        if self.cchar == "{": return ["LBR", "{"]
        if self.cchar == "}": return ["RBR", "}"]
        if self.cchar == "-" and self.peek() == ">":
            self.advance()
            return ["ARW", "->"]

        print("Unknown token.")

class Collector:
    def __init__(self, tokens):
        self.t = tokens
        self.ctok = self.t.next()

    def eat(self, type):
        if self.ctok[0] == type or type == "NIL":
            #tok = self.ctok
            self.ctok = self.t.next()
            #print(str(tok), " -> ", str(self.ctok))
        else: print("Eat failed.")

    def read(self):
        self.data = {'enter':'', 'tables':{}}
        while self.ctok[0] != "END":
            # print(self.ctok)

            if self.ctok[0] == "TOK":
                if self.ctok[1] == "enter":
                    self.eat("TOK")
                    self.eat("ARW")
                    if self.ctok[0] == "TOK":
                        self.data["enter"] = self.ctok[1]

            if self.ctok[0] == "AST":
                self.eat("AST")
                if self.ctok[0] == "TOK":
                    tok = self.ctok
                    self.eat("TOK")
                    if self.ctok[0] == "LBR":
                        self.eat("LBR")
                        self.data["tables"][tok[1]] = []
                        c = -1
                        while True:
                            if self.ctok[0] == "STR":
                                c += 1
                                self.data["tables"][tok[1]].append([self.ctok[1], []])
                                self.eat("STR")
                                if self.ctok[0] == "ARW":
                                    self.eat("ARW")
                                    while self.ctok[0] == "TOK":
                                        self.data["tables"][tok[1]][c][1].append(self.ctok[1])
                                        self.eat("TOK")
                            if self.ctok[0] == "RBR": break
                            #else:
                            #    print("Unrecognized pattern.")
                            #    break




            self.eat("NIL")

        return self.data


class Randomizer:
    def __init__(self, collector):
        self.c = collector
        self.data = self.c.read()

        # pprint(self.data)

    def c_r(self, depth, which):
        c = choice(which)
        t = depth*'. '
        print(f"{t} {c[0]}")
        for s in c[1]:
            self.c_r(depth+1, self.data["tables"][s])

    def go(self):
        if self.data["enter"] == "" or not self.data["enter"] in self.data["tables"]:
            print("Missing or incorrect entrance.")

        self.c_r(0, self.data["tables"][self.data["enter"]])

if __name__ == "__main__":
    with open(argv[1], "r") as file:
        t = Tokenizer("".join(file.readlines()))
        c = Collector(t)
        r = Randomizer(c)
        r.go()
