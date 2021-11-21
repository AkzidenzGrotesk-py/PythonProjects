from sys import argv, exit
from string import ascii_letters, digits as ascii_digits
from os import path

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
    "IDN" : "A",
    "STR" : "\"",
    "ADD" : "+",
    "SUB" : "-",
    "DIV" : "/",
    "MUL" : "*",
    "PRL" : "(",
    "PRR" : ")",
    "EQL" : "=",
    "SMC" : ";",
    "LTA" : "<",
    "GTA" : ">",
    "ATS" : "@",
    "LAW" : "->",
    "COM" : ",",
    "CLL" : "{",
    "CLR" : "}",
    "GTE" : ">=",
    "LTE" : "<=",
    "EQT" : "==",
    "NEQ" : "!=",
    "CLN" : ":"
}
VALID_CHARS = ascii_letters + ascii_digits + "_"

# ---------------------------------
class ErrorHandler:
    def __init__(self):
        self.pos = 0

    def reset_pos(self):
        self.pos = 0

    def token_error(self, description: str):
        print(f"\033[31m[ERROR] @ c:{self.pos} -> {description} in Tokenizer.\033[0m")
        exit(1)

    def construct_error(self, description: str):
        print(f"\033[31m[ERROR] @ t:{self.pos} -> {description} in Constructor.\033[0m")
        exit(1)

    def interpret_error(self, description: str):
        print(f"\033[31m[ERROR] @ n:{self.pos} -> {description} in Interpreter.\033[0m")
        exit(1)

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

    def peek(self):
        if self.cpos + 1 >= len(self.text) - 1:
            return "EOF"
        return self.text[self.cpos + 1]

    def collect_number(self):
        col = ""
        while (self.cchar.isdigit() or self.cchar == ".") and self.cchar != "EOF":
            col += self.cchar
            self.advance()
        if self.cchar != "EOF": self.retreat()
        return float(col) if '.' in col else int(col)

    def collect_identity(self):
        col = ""
        while self.cchar in VALID_CHARS and self.cchar != "EOF":
            col += self.cchar
            self.advance()
        if self.cchar != "EOF": self.retreat()
        return col

    def collect_string(self, entry = "\""):
        col = ""
        self.advance()
        while self.cchar != entry and self.cchar != "EOF":
            col += self.cchar
            self.advance()
        # if self.cchar != "EOF": self.retreat()
        return col

    def get_token(self):
        self.advance()

        while self.cchar in [" ", "\n", "\t", "\r"] and self.cchar != "EOF": self.advance()
        if self.cchar == "EOF": return Token("EOF", None)
        if self.cchar.isdigit() or self.cchar == ".": return Token("NUM", self.collect_number())

        if self.cchar in ["\"", "\'"]: return Token("STR", self.collect_string(self.cchar))

        match self.cchar + self.peek():
            case '->':
                self.advance()
                return Token("LAW", "->")
            case '>=':
                self.advance()
                return Token("GTE", ">=")
            case '<=':
                self.advance()
                return Token("LTE", "<=")
            case '==':
                self.advance()
                return Token("EQT", "==")
            case '!=':
                self.advance()
                return Token("NEQ", "!=")

        match self.cchar:
            case '+': return Token("ADD", "+")
            case '-': return Token("SUB", "-")
            case '/': return Token("DIV", "/")
            case '*': return Token("MUL", "*")
            case '(': return Token("PRL", "(")
            case ')': return Token("PRR", ")")
            case '=': return Token("EQL", "=")
            case ';': return Token("SMC", ";")
            case '<': return Token("LTA", "<")
            case '>': return Token("GTA", ">")
            case '@': return Token("ATS", "@")
            case ',': return Token("COM", ",")
            case '{': return Token("CLL", "{")
            case '}': return Token("CLR", "}")
            case ':': return Token("CLN", ":")

        if self.cchar in VALID_CHARS:
            ident = self.collect_identity()
            if ident == "true": return Token("BTF", True)
            elif ident == "false": return Token("BTF", False)
            return Token("IDN", ident)

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
                if self.tok.type == "MUL":
                    return self.eat_function_call()
                oper = self.eat_expression()
                self.consume("PRR")
                return oper
            case "BTF":
                self.consume("BTF")
                return ASTDataNode("BOOLEAN", ctok.value)
            case "MUL":
                self.consume("MUL")
                return self.eat_function_call()
            case "IDN":
                self.consume("IDN")
                return ASTDataNode("VARIABLE", ctok.value)

        self.eh.construct_error(f"unrecognized symbol is {self.tok.type} when trying to eat factors")

    def eat_term(self):
        node = self.eat_factor()

        while self.tok.type in ["MUL", "DIV"]:
            ctok = self.tok
            if ctok.type == "MUL": self.consume("MUL")
            elif ctok.type == "DIV": self.consume("DIV")
            else: self.eh.construct_error("unrecognized symbol when trying to eat terms")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_factor())

        return node

    def eat_num_expr(self):
        node = self.eat_term()

        while self.tok.type in ["ADD", "SUB"]:
            ctok = self.tok
            if ctok.type == "ADD": self.consume("ADD")
            elif ctok.type == "SUB": self.consume("SUB")

            else: self.eh.construct_error("unrecognized symbol when trying to eat numerical expression")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_term())

        return node

    def eat_num_expression(self):
        node = self.eat_num_expr()

        while self.tok.type in ["LTA", "GTA", "GTE", "LTE", "EQT", "NEQ"]:
            ctok = self.tok
            if ctok.type == "LTA": self.consume("LTA")
            elif ctok.type == "GTA": self.consume("GTA")
            elif ctok.type == "GTE": self.consume("GTE")
            elif ctok.type == "LTE": self.consume("LTE")
            elif ctok.type == "EQT": self.consume("EQT")
            elif ctok.type == "NEQ": self.consume("NEQ")
            else: self.eh.construct_error("unrecognized symbol when trying to eat expression")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_term())

        return node

    def eat_str_elems(self):
        ctok = self.tok
        match self.tok.type:
            case "STR":
                self.consume("STR")
                return ASTDataNode("STRING", ctok.value)
            case "PRL":
                self.consume("PRL")
                if self.tok.type == "MUL":
                    return self.eat_function_call()
                oper = self.eat_expression()
                self.consume("PRR")
                return oper
            case "IDN":
                self.consume("IDN")
                return ASTDataNode("VARIABLE", ctok.value)

        self.eh.construct_error("unrecognized symbol when trying to eat string elements")

    def eat_str_expression(self):
        node = self.eat_str_elems()

        while self.tok.type in ["ADD", "EQT", "NEQ"]:
            ctok = self.tok
            if ctok.type == "ADD": self.consume("ADD")
            elif ctok.type == "EQT": self.consume("EQT")
            elif ctok.type == "NEQ": self.consume("NEQ")
            else: self.eh.construct_error("unrecognized symbol when trying to eat string expression")

            node = ASTMultiNode("STRING_OPERATION", ctok.value, node, self.eat_str_elems())

        return node

    def eat_expression(self):
        if self.tok.type == "STR": return self.eat_str_expression()
        else: return self.eat_num_expression()

    def eat_calculation(self):
        return self.eat_expression()

    def eat_variable_assignment(self, var_name):
        return ASTMultiNode("ASSIGNMENT", "=", ASTDataNode("VARIABLE_NAME", var_name), self.eat_expression())

    def eat_params(self):
        node = ASTListNode("FUNC_PARAMS", [])
        while self.tok.type != "PRR":
            node.add(self.eat_expression())
            if self.tok.type != "PRR": self.consume("COM")
        return node

    def eat_function_call(self):
        self.consume("MUL")
        params = self.eat_params()
        self.consume("PRR")
        self.consume("LAW")
        ctok = self.tok
        self.consume("IDN")
        node = ASTMultiNode("FUNC_CALL", "!", ASTDataNode("FUNC_NAME", ctok.value), params)
        return node

    def eat_branch(self):
        self.consume("CLN")
        expr = self.eat_expression()
        self.consume("CLL")
        cond = ASTListNode("STATEMENTS", [])
        while self.tok.type != "CLR" and self.tok.type != "EOF":
            cond.add(self.eat_statement())
            self.consume("SMC")
        self.consume("CLR")

        cond_else = ASTListNode("STATEMENTS", [])
        if self.tok.type == "IDN" and self.tok.value == "else":
            self.consume("IDN")
            self.consume("CLL")
            while self.tok.type != "CLR" and self.tok.type != "EOF":
                cond_else.add(self.eat_statement())
                self.consume("SMC")
            self.consume("CLR")

        return ASTListNode("CONDITIONAL", [expr, cond, cond_else])

    def eat_while_loop(self):
        self.consume("CLN")
        expr = self.eat_expression()
        self.consume("CLL")
        cond = ASTListNode("STATEMENTS", [])
        while self.tok.type != "CLR" and self.tok.type != "EOF":
            cond.add(self.eat_statement())
            self.consume("SMC")
        self.consume("CLR")

        return ASTListNode("WHILE_LOOP", [expr, cond])

    def eat_function(self, func_name):
        self.consume("PRL")
        self.consume("PRR")
        self.consume("CLL")
        cond = ASTListNode("STATEMENTS", [])
        while self.tok.type != "CLR" and self.tok.type != "EOF":
            cond.add(self.eat_statement())
            self.consume("SMC")
        self.consume("CLR")

        return ASTMultiNode("FUNCTION", "fn", ASTDataNode("FUNC_NAME", func_name), cond)

    def eat_statement(self):
        if self.tok.type == "EQL":
            self.consume("EQL")
            return self.eat_calculation()

        elif self.tok.type == "IDN":
            ctok = self.tok
            self.consume("IDN")

            if self.tok.type == "EQL":
                self.consume("EQL")
                return self.eat_variable_assignment(ctok.value)
            elif ctok.value == "if":
                return self.eat_branch()
            elif ctok.value == "while":
                return self.eat_while_loop()
            else:
                return self.eat_function(ctok.value)
                # self.eh.construct_error(f"unrecognized identity operation, found {self.tok.type}")

        elif self.tok.type == "PRL":
            self.consume("PRL")
            return self.eat_function_call()

        else:
            self.eh.construct_error(f"unrecognized pattern, found {self.tok.type}")

    def construct(self):
        self.eh.reset_pos()
        self.next_tok()
        self.program = ASTListNode("STATEMENTS", [])

        while self.tok.type != "EOF":
            self.program.add(self.eat_statement())
            self.consume("SMC")

        return self.program

class Interpreter:
    def __init__(self, ct: Constructor, eh: ErrorHandler, st: bool = False):
        self.ct = ct
        self.eh = eh
        self.statement_toggle = st
        self.ret_val = 1
        self.breakout = False
        self.breakout_loop = False
        self.memory = {}
        self.function_memory = {}

    def execute(self):
        self.eh.reset_pos()
        return self.traverse(self.ct.construct())

    def traverse(self, node):
        self.eh.pos += 1

        if node.type == "STATEMENTS":
            self.ret_val = 1
            for i, child in enumerate(node.sub_nodes):
                if self.statement_toggle: print(f"[{i + 1}] {self.traverse(child)}")
                else: self.traverse(child)
                if self.breakout: break
            self.breakout = False
            return self.ret_val

        if node.type == "OPERATION":
            match node.value:
                case "+": return self.traverse(node.left) + self.traverse(node.right)
                case "-": return self.traverse(node.left) - self.traverse(node.right)
                case "*": return self.traverse(node.left) * self.traverse(node.right)
                case "/": return self.traverse(node.left) / self.traverse(node.right)
                case ">=": return self.traverse(node.left) >= self.traverse(node.right)
                case "<=": return self.traverse(node.left) <= self.traverse(node.right)
                case ">": return self.traverse(node.left) > self.traverse(node.right)
                case "<": return self.traverse(node.left) < self.traverse(node.right)
                case "==": return self.traverse(node.left) == self.traverse(node.right)
                case "!=": return self.traverse(node.left) != self.traverse(node.right)
                case _: self.eh.interpret_error("unrecognized operator")

        if node.type == "UNARY_OP":
            if node.value == "+": return +self.traverse(node.right)
            elif node.value == "-": return -self.traverse(node.right)
            else: self.eh.interpret_error("unrecognized unary operation")

        if node.type == "NUMBER": return node.value

        if node.type == "ASSIGNMENT":
            self.memory[self.traverse(node.left)] = self.traverse(node.right)
            return 1

        if node.type == "VARIABLE_NAME": return node.value

        if node.type == "VARIABLE":
            if node.value in self.memory:
                return self.memory[node.value]
            else:
                self.eh.interpret_error("variable does not exist")

        if node.type == "FUNC_CALL":
            func_type = self.traverse(node.left)
            params = self.traverse(node.right)
            match func_type:
                case "print":
                    if len(params) > 1:
                        print(params[0], end = '' if params[1] else '\n')
                    else:
                        print(params[0])
                    return 1
                case "get":
                    return input(params[0])
                case "length": return len(params[0])
                case "string": return str(params[0])
                case "int": return int(params[0])
                case "float": return float(params[0])
                case "return":
                    self.ret_val = params[0]
                    if len(params) > 1:
                        self.breakout = params[1]
                    else: self.breakout = True
                    return 1
                case "break":
                    self.breakout_loop = True
                    return 1
                case _:
                    if func_type in self.function_memory:
                        return self.traverse(self.function_memory[func_type])
                    else:
                        self.eh.interpret_error("function does not exist")

        if node.type == "FUNC_NAME": return node.value

        if node.type == "FUNC_PARAMS":
            return [self.traverse(n) for n in node.sub_nodes]

        if node.type == "STRING": return node.value

        if node.type == "STRING_OPERATION":
            if node.value == "+": return self.traverse(node.left) + self.traverse(node.right)
            elif node.value == "==": return self.traverse(node.left) == self.traverse(node.right)
            elif node.value == "!=": return self.traverse(node.left) != self.traverse(node.right)
            else: self.eh.interpret_error("unrecognized string operator")

        if node.type == "BOOLEAN": return node.value

        if node.type == "CONDITIONAL":
            if self.traverse(node.sub_nodes[0]):
                self.traverse(node.sub_nodes[1])
            else:
                self.traverse(node.sub_nodes[2])
            return 1

        if node.type == "WHILE_LOOP":
            while self.traverse(node.sub_nodes[0]) and not self.breakout_loop:
                self.traverse(node.sub_nodes[1])
            self.breakout_loop = False

            return 1

        if node.type == "FUNCTION":
            self.function_memory[self.traverse(node.left)] = node.right
            return 1

        self.eh.interpret_error(f"unrecognized node is {node.type}")

# ---------------------------------
def main() -> None:
    out = True if "--out" in argv else False
    eh = ErrorHandler()

    if len(argv) > 1:
        if path.exists(argv[1]):
            with open(argv[1], "r") as code_file:
                code = "".join(code_file.readlines())
            t = Tokenizer(code.replace("\\n", "\n"), eh)
            c = Constructor(t, eh)
            i = Interpreter(c, eh, out)
            i.execute()

    else:
        while True:
            user = input("~> ")
            if user.strip() == "": break
            t = Tokenizer(user, eh)
            c = Constructor(t, eh)
            i = Interpreter(c, eh, out)
            i.execute()

if __name__ == "__main__":
    main()
