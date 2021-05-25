import sys, string

WHITESPACE = [" ", "\n", "\t", "\r", "\b", "\f"]
RESERVEDKEYS = ["BEGIN","do","next","then","END","else","nil","true","alias","elsif","not","undef","and","end","or","unless","begin","ensure","redo","until","break","false","rescue","when","case","for","retry","while","class","if","return","def","in","self","__FILE__","defined?","module","super","__LINE__"]
LEGALCHARS = string.ascii_letters + string.digits + "~_"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self): return f"(\033[35m{self.type}\033[0m, {self.value})"
    def __str__(self): return self.__repr__()

class ASTMultiNode:
    def __init__(self, type, subs):
        self.type = type
        self.subs = subs

    def __repr__(self):
        o = "{\n"
        for s in self.subs:
            o += s.__repr__() + "\n"
        o += "}"
        return o

    def __str__(self): return self.__repr__()

class ASTLeftRightNode:
    def __init__(self, type, left, value, right):
        self.type = type
        self.left = left
        self.value = value
        self.right = right

    def __repr__(self): return f"[{self.left.__repr__()}, {self.value}, {self.right.__repr__()}]"
    def __str__(self): return self.__repr__()

class ASTDataNode:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self): return f"{self.value}"
    def __str__(self): return self.__repr__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.line = 1
        self.pos = 0
        self.cchar = [-1, None]

    ##### ERRORS
    def error(self, id, msg):
        print(f"\033[31m(L{str(id)}) error @ line {self.line} char {self.pos}: {msg}.\033[0m")
        sys.exit()

    ##### CHARACTERS
    def peek(self): return self.text[self.cchar[0] + 1]

    def update_char(self):
        if self.cchar[0] > (len(self.text) - 1):
            self.cchar[1] = ""
        else:
            self.cchar[1] = self.text[self.cchar[0]]

    def forward(self):
        self.cchar[0] += 1
        self.pos += 1
        self.update_char()

    def back(self):
        self.cchar[0] -= 1
        self.pos -= 1
        self.update_char()

    def this(self): return self.cchar[1]

    ##### UTILITY
    def whitespace(self):
        while self.this() in WHITESPACE and self.this() != "":
            if self.this() == "\n":
                self.line += 1
                self.pos = 0
            self.forward()

    def numerical(self):
        o = ""
        while self.this().isnumeric() and self.this() != "":
            o += self.this()
            self.forward()
        self.back()
        return int(o)

    def id(self):
        o = ""
        while self.this() in LEGALCHARS and self.this() != "":
            o += self.this()
            self.forward()
        self.back()
        return o

    def comment(self):
        self.forward()
        while self.this() != "\n":
            self.forward()
        self.line += 1
        self.pos = 0

    def string(self, check):
        o = ""
        self.forward()
        while self.this() != check and self.this() != "":
            o += self.this()
            self.forward()
        return o

    ##### GET NEXT TOKEN
    def next(self):
        self.forward()

        if self.this() in WHITESPACE: self.whitespace()
        if self.this() == "#": self.comment()
        if self.this() == "": return Token("EOFILE", "")

        if self.this().isnumeric(): return Token("NUMBER", self.numerical())
        if self.this() in LEGALCHARS: return Token("IDENTF", self.id())
        if self.this() == "\"" or self.this() == "\'": return Token("STRING", self.string(self.this()))

        if self.this() == "+": return Token("OPRADD", "+")
        if self.this() == "-": return Token("OPRSUB", "-")
        if self.this() == "*": return Token("OPRMUL", "*")
        if self.this() == "/": return Token("OPRDIV", "/")
        if self.this() == "=": return Token("OPREQL", "=")
        if self.this() == "(": return Token("LPAREN", "(")
        if self.this() == ")": return Token("RPAREN", ")")
        if self.this() == "{": return Token("LCURLY", "{")
        if self.this() == "}": return Token("RCURLY", "}")
        if self.this() == ";": return Token("SEMICL", ";")
        if self.this() == ".": return Token("SUBDOT", ".")

        if self.this() in WHITESPACE or self.this() == "#" or self.this() == "":
            return self.next()

        self.error(1, "Unrecognized token")


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.ctok = None
        self.pos = -1

    ##### ERRORS
    def error(self, id, msg):
        print(f"\033[31m(P{str(id)}) error @ token {self.pos}: {msg}.\033[0m")
        sys.exit()

    ##### UTILITY
    def next(self):
        self.ctok = self.lexer.next()

    def consume(self, type):
        # print(self.ctok)
        if self.ctok.type == type:
            self.next()
            self.pos += 1

        else:
            self.error(1, f"Token has not been consumed correctly. '{type}' tested against '{self.ctok.type}'")

    ##### MAIN PARSING
    def factor(self, alt_mode = 0):
        ctoken = self.ctok
        if self.ctok.type == "NUMBER":
            self.consume("NUMBER")
            return ASTDataNode("NUMBER", ctoken.value)
        if self.ctok.type == "OPRADD":
            self.consume("OPRADD")
            return ASTLeftRightNode("UNARYOP", None, "+", self.factor())
        if self.ctok.type == "OPRSUB":
            self.consume("OPRSUB")
            return ASTLeftRightNode("UNARYOP", None, "-", self.factor())
        if self.ctok.type == "LPAREN":
            self.consume("LPAREN")
            oper = self.string_or_int_expression(ctoken)
            self.consume("RPAREN")
            return oper
        if self.ctok.type == "IDENTF":
            self.consume("IDENTF")
            if alt_mode == 0: return ASTDataNode("VARIABLE", ctoken.value)
            elif alt_mode == 1:
                return ctoken.value

        self.error(3, "Unrecognized symbol in factor()")

    def term(self):
        node = self.factor()

        while self.ctok.type in ["OPRMUL", "OPRDIV", "SUBDOT"]:
            ctoken = self.ctok
            r = 0
            if ctoken.type == "OPRMUL": self.consume("OPRMUL")
            elif ctoken.type == "OPRDIV": self.consume("OPRDIV")
            elif ctoken.type == "SUBDOT":
                r = 1
                self.consume("SUBDOT")
            else: self.error(4, "Unrecognized symbol in term()")

            node = ASTLeftRightNode("OPERATION", node, ctoken.value, self.factor(r))

        return node

    def expr(self):
        node = self.term()

        while self.ctok.type in ["OPRADD", "OPRSUB"]:
            ctoken = self.ctok
            if ctoken.type == "OPRADD": self.consume("OPRADD")
            elif ctoken.type == "OPRSUB": self.consume("OPRSUB")
            else: self.error(5, "Unrecognized symbol in expr()")

            node = ASTLeftRightNode("OPERATION", node, ctoken.value, self.term())

        return node

    def strterm(self, identfreturntype = 0):
        ctoken = self.ctok
        if self.ctok.type == "IDENTF":
            self.consume("IDENTF")
            if identfreturntype == 0: return ASTDataNode("VARIABLE", ctoken.value)
            if identfreturntype == 1:
                return ctoken.value
        if self.ctok.type == "STRING":
            self.consume("STRING")
            return ASTDataNode("STRING", ctoken.value)

        self.error(8, "Unrecognized pattern in strterm()")

    def strexpr(self):
        node = self.strterm()

        while self.ctok.type in ["OPRADD", "SUBDOT"]:
            ctoken = self.ctok
            r = 0
            if self.ctok.type == "OPRADD": self.consume("OPRADD")
            if self.ctok.type == "SUBDOT":
                r = 1
                self.consume("SUBDOT")

            node = ASTLeftRightNode("STROPERATION", node, ctoken.value, self.strterm(r))

        return node

    def string_or_int_expression(self, ctoken):
        if self.ctok.type == "STRING":
            return self.strexpr()
        elif self.ctok.type in ["OPRADD", "OPRSUB", "NUMBER", "IDENTF", "LPAREN"]:
            expr = self.expr()
            return expr
        else:
            self.error(7, "Unrecognized pattern check between operation and string")


    def eat_assignment(self, ctoken):
        self.consume("OPREQL")
        self.program.subs.append(ASTLeftRightNode("ASSIGNMENT", ctoken.value, "=", self.string_or_int_expression(ctoken)))

    def eat_func_puts(self, ctoken):
        if self.ctok.type == "LPAREN":
            self.consume("LPAREN")
            self.program.subs.append(ASTLeftRightNode("BUILTIN", None, "puts", self.string_or_int_expression(ctoken)))
            self.consume("RPAREN")
        else:
            self.program.subs.append(ASTLeftRightNode("BUILTIN", None, "puts", self.string_or_int_expression(ctoken)))

    def eat_statement(self):
        if self.ctok.type == "IDENTF":
            ctoken = self.ctok
            self.consume("IDENTF")

            if self.ctok.type == "OPREQL": self.eat_assignment(ctoken)
            elif ctoken.value == "puts": self.eat_func_puts(ctoken)
            else: self.error(6, "Unrecognized token after identifier")

        else: self.error(2, "Unrecognized pattern in parser")

    def parse(self):
        self.next()
        self.program = ASTMultiNode("STATEMENTS", [])

        while self.ctok.type != "EOFILE":
            self.eat_statement()
            if self.ctok.type == "SEMICL": self.consume("SEMICL")

        return self.program



class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.mem = {}

    def error(self, id, msg):
        print(f"\033[31m(I{str(id)}) error: {msg}.\033[0m")
        sys.exit()

    def traverse(self, node):
        if node.type == "STATEMENTS":
            for j, child in enumerate(node.subs):
                #print(f"[{j}] {self.traverse(child)}")
                self.traverse(child)

            return True

        if node.type == "OPERATION":
            if node.value == "+": return self.traverse(node.left) + self.traverse(node.right)
            elif node.value == "-": return self.traverse(node.left) - self.traverse(node.right)
            elif node.value == "/": return self.traverse(node.left) / self.traverse(node.right)
            elif node.value == "*": return self.traverse(node.left) * self.traverse(node.right)
            elif node.value == ".":
                if node.right == "size": return len(str(self.traverse(node.left)))
                else: self.error(9, "Unrecognized integer data")
            else: self.error(1, "Unrecognized OPERATION operator")

        if node.type == "UNARYOP":
            if node.value == "+": return +self.traverse(node.right)
            elif node.value == "-": return -self.traverse(node.right)
            else: self.error(2, "Unrecognized UNARYOP operator")

        if node.type == "NUMBER": return node.value

        if node.type == "ASSIGNMENT":
            if node.value == "=":
                s = self.traverse(node.right)
                self.mem[node.left] = s
                return s
            else: self.error(4, "Unrecognized ASSIGNMENT operator")

        if node.type == "VARIABLE":
            if node.value in self.mem:
                return self.mem[node.value]
            else: self.error(5, "Variable is not defined")

        if node.type == "BUILTIN":
            if node.value == "puts":
                s = self.traverse(node.right)
                print(s)
                return s
            else: self.error(6, "Unknown built-in function")

        if node.type == "STRING": return node.value

        if node.type == "STROPERATION":
            if node.value == "+": return str(self.traverse(node.left)) + str(self.traverse(node.right))
            if node.value == ".":
                if node.right == "size": return len(self.traverse(node.left))
                elif node.right == "upcase": return self.traverse(node.left).upper()
                elif node.right == "downcase": return self.traverse(node.left).lower()
                elif node.right == "to_i": return int(self.traverse(node.left))
                else: self.error(7, "Unrecognized string data")

        self.error(3, "Unrecognized syntax node")

    def eval(self):
        self.traverse(self.parser.parse())



if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as pfile:
            text = "".join(pfile.readlines())

        l = Lexer(text)
        p = Parser(l)
        i = Interpreter(p)
        i.eval()

    '''while True:
        text = input("\033[33m. ")
        print("\033[0m", end = '')
        '''
