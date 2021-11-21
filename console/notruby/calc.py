# Cleaned up calculator part.

import sys

# ---------------------------------
class Token:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"(\033[33m{self.type}\033[0m, {self.value})"

    def __str__(self): return self.__repr__()

class ASTDataNode:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"(\033[33m{self.type}\033[0m, {self.value})"

    def __str__(self): return self.__repr__()

class ASTMultiNode:
    def __init__(self, type: str, value: str, left: ASTDataNode, right: ASTDataNode):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"(\033[33m{self.type}\033[0m, {self.value}, {self.left.__repr__()}, {self.right.__repr__()})"

    def __str__(self): return self.__repr__()

class ASTListNode:
    def __init__(self, type: str, sub_nodes):
        self.type = type
        self.sub_nodes = sub_nodes

    def add(self, new_node):
        self.sub_nodes.append(new_node)

    def __repr__(self):
        sns = ", ".join([sn.__repr__() for sn in self.sub_nodes])
        return f"(\033[33m{self.type}\033[0m, {sns})"

    def __str__(self): return self.__repr__()

# ---------------------------------
TOKENS = {
    "EOF" : None,
    "NUM" : 0,
    "ADD" : "+",
    "SUB" : "-",
    "DIV" : "/",
    "MUL" : "*",
    "PRL" : "(",
    "PRR" : ")",
    "EQL" : "=",
    "SMC" : ";"
}

# ---------------------------------
class ErrorHandler:
    def __init__(self):
        self.pos = 0

    def reset_pos(self):
        self.pos = 0

    def token_error(self, description: str):
        print(f"\033[31m[ERROR] @ c:{self.pos} -> {description} in Tokenizer.\033[0m")
        sys.exit(1)

    def construct_error(self, description: str):
        print(f"\033[31m[ERROR] @ t:{self.pos} -> {description} in Constructor.\033[0m")
        sys.exit(1)

    def interpret_error(self, description: str):
        print(f"\033[31m[ERROR] @ n:{self.pos} -> {description} in Interpreter.\033[0m")
        sys.exit(1)

class Tokenizer:
    def __init__(self, text: str, eh: ErrorHandler):
        self.text = text
        self.eh = eh
        self.cpos = -1
        self.cchar = None

    def advance(self):
        if self.cpos >= len(self.text) - 1:
            self.cchar = "EOF"
            return
        else:
            self.cpos += 1
            self.eh.pos += 1
            self.cchar = self.text[self.cpos]

    def retreat(self):
        if self.cpos <= 0: return
        else:
            self.cpos -= 1
            self.eh.pos -= 1
            self.cchar = self.text[self.cpos]

    def collect_number(self):
        col = ""
        while (self.cchar.isdigit() or self.cchar == ".") and self.cchar != "EOF":
            col += self.cchar
            self.advance()
        if self.cchar != "EOF": self.retreat()
        return float(col) if '.' in col else int(col)

    def get_token(self):
        self.advance()

        while self.cchar in [" ", "\n", "\t", "\r"] and self.cchar != "EOF": self.advance()
        if self.cchar == "EOF": return Token("EOF", None)
        if self.cchar.isdigit() or self.cchar == ".": return Token("NUM", self.collect_number())

        match self.cchar:
            case '+': return Token("ADD", "+")
            case '-': return Token("SUB", "-")
            case '/': return Token("DIV", "/")
            case '*': return Token("MUL", "*")
            case '(': return Token("PRL", "(")
            case ')': return Token("PRR", ")")
            case '=': return Token("EQL", "=")
            case ';': return Token("SMC", ";")

        self.eh.token_error("token not recognized")

class Constructor:
    def __init__(self, ti: Tokenizer, eh: ErrorHandler):
        self.ti = ti
        self.eh = eh
        self.tok = Token("NON", None)

    def next_tok(self):
        self.tok = self.ti.get_token()

    def consume(self, type: str):
        if self.tok.type == type:
            self.next_tok()
            self.eh.pos += 1

        else:
            self.eh.construct_error(f"token has not been consumed correctly, looking for {type} ({TOKENS[type]}) found {self.tok.type}")

    def eat_factor(self):
        ctok = self.tok
        match self.tok.type:
            case "NUM":
                self.consume("NUM")
                return ASTDataNode("NUMBER", ctok.value)
            case "ADD":
                self.consume("ADD")
                return ASTMultiNode("UNARY_OP", "+", None, self.eat_factor())
            case "SUB":
                self.consume("SUB")
                return ASTMultiNode("UNARY_OP", "-", None, self.eat_factor())
            case "PRL":
                self.consume("PRL")
                oper = self.eat_expression()
                self.consume("PRR")
                return oper

        self.eh.construct_error("unrecognized symbol when trying to eat factors")

    def eat_term(self):
        node = self.eat_factor()

        while self.tok.type in ["MUL", "DIV"]:
            ctok = self.tok
            if ctok.type == "MUL": self.consume("MUL")
            elif ctok.type == "DIV": self.consume("DIV")
            else: self.eh.construct_error("unrecognized symbol when trying to eat terms")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_factor())

        return node

    def eat_expression(self):
        node = self.eat_term()

        while self.tok.type in ["ADD", "SUB"]:
            ctok = self.tok
            if ctok.type == "ADD": self.consume("ADD")
            elif ctok.type == "SUB": self.consume("SUB")
            else: self.eh.construct_error("unrecognized symbol when trying to eat expression")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_term())

        return node

    def eat_calculation(self):
        self.program.add(self.eat_expression())

    def eat_statement(self):
        if self.tok.type == "EQL":
            self.consume("EQL")
            self.eat_calculation()

        else:
            self.eh.construct_error(f"unrecognized pattern, found {self.tok.type}")

    def construct(self):
        self.eh.reset_pos()
        self.next_tok()
        self.program = ASTListNode("STATEMENTS", [])

        while self.tok.type != "EOF":
            self.eat_statement()
            self.consume("SMC")

        return self.program

class Interpreter:
    def __init__(self, ct: Constructor, eh: ErrorHandler):
        self.ct = ct
        self.eh = eh

    def execute(self):
        self.eh.reset_pos()
        return self.traverse(self.ct.construct())

    def traverse(self, node):
        self.eh.pos += 1

        if node.type == "STATEMENTS":
            for i, child in enumerate(node.sub_nodes):
                print(f"[{i + 1}] {self.traverse(child)}")
                # self.traverse(child)
            return 1

        if node.type == "OPERATION":
            if node.value == "+": return self.traverse(node.left) + self.traverse(node.right)
            elif node.value == "-": return self.traverse(node.left) - self.traverse(node.right)
            elif node.value == "*": return self.traverse(node.left) * self.traverse(node.right)
            elif node.value == "/": return self.traverse(node.left) / self.traverse(node.right)
            else: self.eh.interpret_error("unrecognized operator")

        if node.type == "UNARY_OP":
            if node.value == "+": return +self.traverse(node.right)
            elif node.value == "-": return -self.traverse(node.right)
            else: self.eh.interpret_error("unrecognized unary operation")

        if node.type == "NUMBER": return node.value

        self.eh.interpret_error("unrecognized node")

# ---------------------------------
def main() -> None:
    user = input("> ")
    eh = ErrorHandler()
    t = Tokenizer(user, eh)
    c = Constructor(t, eh)
    i = Interpreter(c, eh)
    i.execute()

if __name__ == "__main__":
    main()
