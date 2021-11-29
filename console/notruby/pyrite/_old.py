import sys
from os import path
from string import ascii_letters, digits as ascii_digits

# ---------------------------------
# :: CONSTANTS ::
# ---------------------------------
TOKENS = {
    "EOF" : None,
    "NUM" : 0,
    "IDN" : "A",
    "STR" : "\"",
    "NWL" : "\\n",
    "ADD" : "+",
    "SUB" : "-",
    "DIV" : "/",
    "MUL" : "*",
    "POW" : "**",
    "PER" : "%",
    "EQLS" : "==",
    "NEQL" : "!=",
    "GTH" : ">",
    "LTH" : "<",
    "GTHE" : ">=",
    "LTHE" : "<=",
    "COMB" : "<=>",
    "CEQL" : "===",
    "PRL" : "(",
    "PRR" : ")",
    "EQL" : "=",
    "COM" : ",",
    "SMC" : ";",
    "DOT" : ".",
    "AND" : "&&",
    "ORO" : "||",
    "NOT" : "!",
    "BOOL" : False
}
VALID_CHARS = ascii_letters + ascii_digits + "_$"
REPLACEMENTS = {
    True : "true",
    False : "false",
    None : "nil"
}
NOADD_TYPES = ["NONETYPE"]





# ---------------------------------
# :: TOKEN CLASS ::
# ---------------------------------
class Token:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"(\033[33m{self.type}\033[0m, {self.value})"

    def __str__(self): return self.__repr__()





# ---------------------------------
# :: ASTDATANODE CLASS ::
# ---------------------------------
class ASTDataNode:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"(\033[33m{self.type}\033[0m, {self.value})"

    def __str__(self): return self.__repr__()





# ---------------------------------
# :: ASTMULTINODE CLASS ::
# ---------------------------------
class ASTMultiNode:
    def __init__(self, type: str, value: str, left: ASTDataNode, right: ASTDataNode):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"(\033[33m{self.type}\033[0m, {self.value}, {self.left.__repr__()}, {self.right.__repr__()})"

    def __str__(self): return self.__repr__()





# ---------------------------------
# :: ASTLISTNODE CLASS ::
# ---------------------------------
class ASTListNode:
    def __init__(self, type: str, sub_nodes):
        self.type = type
        self.sub_nodes = sub_nodes

    def add(self, new_node):
        if new_node.type not in NOADD_TYPES:
            self.sub_nodes.append(new_node)

    def __repr__(self):
        sns = ",\n\t".join([sn.__repr__() for sn in self.sub_nodes])
        return f"(\033[33m{self.type}\033[0m,\n\t{sns}\n\t)"

    def __str__(self): return self.__repr__()










# ---------------------------------
# :: ERRORHANDLER CLASS ::
# ---------------------------------
class ErrorHandler:
    def __init__(self, end_on_error = True):
        self.pos = 0
        self.eoe = end_on_error

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








# ---------------------------------
# :: TOKENIZER CLASS ::
# ---------------------------------
class Tokenizer:
    def __init__(self, text: str, eh: ErrorHandler):
        self.text = text
        self.eh = eh
        self.cpos = -1
        self.cchar = None
        self.buffer = []

    def advance(self):
        if self.cpos >= len(self.text) - 1:
            self.cchar = "EOF"
            return

        self.cpos += 1
        self.eh.pos += 1
        self.cchar = self.text[self.cpos]

    def retreat(self):
        if self.cpos <= 0: return

        self.cpos -= 1
        self.eh.pos -= 1
        self.cchar = self.text[self.cpos]

    def peek(self):
        if self.cpos + 1 >= len(self.text) - 1:
            return "EOF"
        return self.text[self.cpos + 1]

    def dob_peek(self):
        if self.cpos + 2 >= len(self.text) - 1:
            return "EOF"
        return self.text[self.cpos + 1] + self.text[self.cpos + 2]

    def collect_number(self):
        col = ""
        while (self.cchar.isdigit() or self.cchar == ".") and self.cchar != "EOF":
            if self.cchar == ".":
                if not self.peek().isdigit():
                    break
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
        while self.cchar not in [entry, "EOF"]:
            if self.cchar + self.peek() == "#{":
                self.advance()
                self.advance()
                v = self.collect_identity()
                self.advance()
                if self.cchar == "}": self.advance()
                else: self.eh.token_error(f"missing closing operator, found {self.cchar}")
                self.buffer.extend([
                    Token("STR", col),
                    Token("ADD", "+"),
                    Token("IDN", v),
                    Token("DOT", "."),
                    Token("IDN", "to_s"),
                    Token("ADD", "+")
                ])
                col = ""

                if self.cchar == entry:
                    return ""

            col += self.cchar

            if self.cchar == "\n":
                self.eh.token_error("will not collect string past newline")

            self.advance()
        # if self.cchar != "EOF": self.retreat()
        return col

    def get_token(self, prev = None):
        if len(self.buffer) > 0:
            return self.buffer.pop(0)

        self.advance()

        while self.cchar in [" ", "\t", "\r"] and self.cchar != "EOF":
            self.advance()

        if self.cchar == "\n":
            return Token("NWL", "\n")

        if self.cchar == "EOF":
            return Token("EOF", None)

        if self.cchar.isdigit():
            return Token("NUM", self.collect_number())

        if self.cchar in ["\"", "\'"]:
            string = self.collect_string(self.cchar)
            if len(self.buffer) > 0:
                self.buffer.append(Token("STR", string))
                return self.buffer.pop(0)
            return Token("STR", string)


        match self.cchar + self.dob_peek():
            case "<=>":
                self.advance()
                self.advance()
                return Token("COMB", "<=>")
            case "===":
                self.advance()
                self.advance()
                return Token("CEQL", "===")
            case "**=":
                self.advance()
                self.advance()
                self.buffer.extend([prev, Token("POW", "**")])
                return Token("EQL", "=")

        match self.cchar + self.peek():
            case '**':
                self.advance()
                return Token("POW", "**")
            case '==':
                self.advance()
                return Token("EQLS", "==")
            case '!=':
                self.advance()
                return Token("NEQL", "!=")
            case '>=':
                self.advance()
                return Token("GTHE", ">=")
            case '<=':
                self.advance()
                return Token("LTHE", "<=")
            case '+=':
                self.advance()
                self.buffer.extend([prev, Token("ADD", "+")])
                return Token("EQL", "=")
            case '-=':
                self.advance()
                self.buffer.extend([prev, Token("SUB", "-")])
                return Token("EQL", "=")
            case '*=':
                self.advance()
                self.buffer.extend([prev, Token("MUL", "*")])
                return Token("EQL", "=")
            case '/=':
                self.advance()
                self.buffer.extend([prev, Token("DIV", "/")])
                return Token("EQL", "=")
            case '%=':
                self.advance()
                self.buffer.extend([prev, Token("PER", "%")])
                return Token("EQL", "=")
            case '&&':
                self.advance()
                return Token("AND", "&&")
            case '||':
                self.advance()
                return Token("ORO", "||")

        match self.cchar:
            case '+': return Token("ADD", "+")
            case '-': return Token("SUB", "-")
            case '/': return Token("DIV", "/")
            case '*': return Token("MUL", "*")
            case '(': return Token("PRL", "(")
            case ')': return Token("PRR", ")")
            case '=': return Token("EQL", "=")
            case ';': return Token("SMC", ";")
            case ',': return Token("COM", ",")
            case '.': return Token("DOT", ".")
            case '%': return Token("PER", "%")
            case '>': return Token("GTH", ">")
            case '<': return Token("LTH", "<")
            case '!': return Token("NOT", "!")

        if self.cchar in VALID_CHARS:
            ident = self.collect_identity()

            match ident:
                case 'or': return Token("ORO", "||")
                case 'and': return Token("AND", "&&")
                case 'not': return Token("NOT", "!")
                case 'true': return Token("BOOL", True)
                case 'false': return Token("BOOL", False)
                case _: return Token("IDN", ident)

        self.eh.token_error("token not recognized")









# ---------------------------------
# :: CONSTRUCTOR CLASS ::
# ---------------------------------
class Constructor:
    def __init__(self, ti: Tokenizer, eh: ErrorHandler, show_consumes: int = 0):
        self.ti = ti
        self.eh = eh
        self.show_consumes = show_consumes
        self.ltok = Token("NON", None)
        self.tok = Token("NON", None)
        self.program = ASTListNode("STATEMENTS", [])

        if show_consumes:
            print("\033[32m[CONSUMPTIONS]\033[0m")

    def next_tok(self):
        self.ltok = self.tok
        self.tok = self.ti.get_token(self.ltok)

    def consume(self, type: str):
        if self.tok.type == type:
            if self.show_consumes: print(self.tok)
            self.next_tok()
            self.eh.pos += 1

        else:
            self.eh.construct_error(f"token has not been consumed correctly,\
             looking for {type} ({TOKENS[type]}) found {self.tok.type}")

    def eat_factor(self):
        ctok = self.tok
        match self.tok.type:
            case "NUM":
                self.consume("NUM")
                return ASTDataNode("NUMBER", ctok.value)
            case "BOOL":
                self.consume("BOOL")
                return ASTDataNode("BOOLEAN", ctok.value)
            case "ADD":
                self.consume("ADD")
                return ASTMultiNode("UNARY_OP", "+", None, self.eat_factor())
            case "SUB":
                self.consume("SUB")
                return ASTMultiNode("UNARY_OP", "-", None, self.eat_factor())
            case "NOT":
                self.consume("NOT")
                return ASTMultiNode("UNARY_OP", "!", None, self.eat_factor())
            case "PRL":
                self.consume("PRL")
                oper = self.eat_operation()
                self.consume("PRR")
                return oper
            case "STR":
                self.consume("STR")
                return ASTDataNode("STRING", ctok.value)
            case "IDN":
                last_tok = self.ltok
                self.consume("IDN")
                if last_tok.type == "DOT":
                    return ASTDataNode("FUNC_NAME", ctok.value)
                return ASTDataNode("VARIABLE", ctok.value)

        self.eh.construct_error(
            f"unrecognized symbol is {self.tok.type} when trying to eat factors"
        )

    def eat_power(self):
        node = self.eat_factor()

        while self.tok.type in ["POW", "DOT"]:
            ctok = self.tok
            if ctok.type == "POW": self.consume("POW")
            elif ctok.type == "DOT": self.consume("DOT")
            else: self.eh.construct_error("unrecognized symbol when trying to eat powers")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_factor())

        return node

    def eat_term(self):
        node = self.eat_power()

        while self.tok.type in ["MUL", "DIV", "PER"]:
            ctok = self.tok
            if ctok.type == "MUL":
                self.consume("MUL")
            elif ctok.type == "DIV":
                self.consume("DIV")
            elif ctok.type == "PER":
                self.consume("PER")
            else: self.eh.construct_error("unrecognized symbol when trying to eat terms")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_power())

        return node

    def eat_expression(self):
        node = self.eat_term()

        while self.tok.type in ["ADD", "SUB"]:
            ctok = self.tok
            if ctok.type == "ADD":
                self.consume("ADD")
            elif ctok.type == "SUB":
                self.consume("SUB")
            else: self.eh.construct_error("unrecognized symbol when trying to eat expression")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_term())

        return node

    def eat_equalities(self):
        node = self.eat_expression()

        while self.tok.type in ["EQLS", "NEQL", "GTHE", "LTHE", "COMB", "CEQL", "GTH", "LTH"]:
            ctok = self.tok

            if ctok.type == "EQLS":
                self.consume("EQLS")
            elif ctok.type == "NEQL":
                self.consume("NEQL")
            elif ctok.type == "GTHE":
                self.consume("GTHE")
            elif ctok.type == "LTHE":
                self.consume("LTHE")
            elif ctok.type == "COMB":
                self.consume("COMB")
            elif ctok.type == "CEQL":
                self.consume("CEQL")
            elif ctok.type == "GTH":
                self.consume("GTH")
            elif ctok.type == "LTH":
                self.consume("LTH")
            else: self.eh.construct_error("unrecognized symbol when trying to eat equality")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_expression())

        return node

    def eat_andornot(self):
        node = self.eat_equalities()

        while self.tok.type in ["AND", "NOT", "ORO"]:
            ctok = self.tok
            if ctok.type == "AND":
                self.consume("AND")
            elif ctok.type == "ORO":
                self.consume("ORO")
            else: self.eh.construct_error("unrecognized symbol when trying to eat AND OR NOT")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_equalities())

        return node

    def eat_inlines(self):
        node = self.eat_andornot()

        while self.tok.type == "IDN" and self.tok.value in ["if", "unless"]:
            ctok = self.tok
            self.consume("IDN")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_andornot())

        return node

    def eat_operation(self):
        return self.eat_inlines()

    def eat_params(self, look_for = "NWL"):
        node = ASTListNode("FUNC_PARAMS", [])
        while self.tok.type not in [look_for, "EOF"]:
            node.add(self.eat_operation())
            if self.tok.type not in [look_for, "EOF", "SMC"]:
                self.consume("COM")
        if look_for not in ["NWL", "EOF"]:
            self.consume(look_for)

        return node

    def eat_variable_assignment(self, var_name):
        return ASTMultiNode("ASSIGNMENT", "=",
            ASTDataNode("VARIABLE_NAME", var_name),
            self.eat_operation())

    def eat_function(self, func_name):
        f_params = ASTListNode("FUNCTION_ARGS", [])

        if self.tok.type == "PRL":
            self.consume("PRL")

            while self.tok.type not in ["PRR", "EOF"]:
                ctok = self.tok
                if self.tok.type == "IDN":
                    self.consume("IDN")
                    f_params.add(ASTDataNode("VARIABLE_NAME", ctok.value))
                if self.tok.type not in ["PRR", "EOF"]:
                    self.consume("COM")

            self.consume("PRR")
        self.consume("NWL")

        acts = ASTListNode("STATEMENTS", [])
        while self.tok.type != "EOF" and (self.tok.value != "end" and self.tok.type == "IDN"):
            acts.add(self.eat_statement())
            if self.tok.type == "SMC":
                self.consume("SMC")
            elif self.tok.type == "NWL":
                self.consume("NWL")
            elif self.tok.type == "EOF":
                break
            else: self.eh.construct_error(f"line ended with incorrect character ({self.tok.value})")
        self.consume("IDN")

        return ASTListNode("FUNCTION", [ASTDataNode("FUNC_NAME", func_name), f_params, acts])
        #return ASTMultiNode("FUNCTION", "fn", ASTDataNode("FUNC_NAME", func_name), acts)

    def eat_cond_unless(self):
        if_expr = self.eat_operation()
        if self.tok.value == "then":
            self.consume("IDN")
        ifevents = ASTListNode("STATEMENTS", [])
        elseevents = ASTListNode("STATEMENTS", [])

        while self.tok.value not in ["else", "end"] and self.tok.type != "EOF":
            ifevents.add(self.eat_statement())
            if self.tok.type == "SMC":
                self.consume("SMC")
            elif self.tok.type == "NWL":
                self.consume("NWL")
            elif self.tok.type == "EOF":
                break
            else: self.eh.construct_error(f"line ended with incorrect character")

        if self.tok.value == "end":
            self.consume("IDN")
            return ASTListNode("UNLESS_CONDITIONAL", [[if_expr, ifevents], elseevents])

        if self.tok.value == "else":
            self.consume("IDN")

            while self.tok.value != "end" and self.tok.type != "EOF":
                elseevents.add(self.eat_statement())
                if self.tok.type == "SMC": self.consume("SMC")
                elif self.tok.type == "NWL": self.consume("NWL")
                elif self.tok.type == "EOF": break
                else: self.eh.construct_error(f"line ended with incorrect character")

        self.consume("IDN")
        return ASTListNode("UNLESS_CONDITIONAL", [[if_expr, ifevents], elseevents])

    def eat_conditional(self):
        if_expr = self.eat_operation()
        if self.tok.value == "then": self.consume("IDN")
        ifevents = ASTListNode("STATEMENTS", [])
        elseevents = ASTListNode("STATEMENTS", [])
        elsifs = []

        while self.tok.value != "end" and self.tok.type != "EOF":
            while self.tok.value not in ["else", "elsif", "end"] and self.tok.type != "EOF":
                ifevents.add(self.eat_statement())
                if self.tok.type == "SMC": self.consume("SMC")
                elif self.tok.type == "NWL": self.consume("NWL")
                elif self.tok.type == "EOF": break
                else: self.eh.construct_error(f"line ended with incorrect character")

            if self.tok.value == "end":
                self.consume("IDN")
                return ASTListNode("CONDITIONAL", [[if_expr, ifevents], elsifs, elseevents])

            if self.tok.value == "elsif":
                while self.tok.value not in ["else", "end"] and self.tok.type != "EOF":
                    self.consume("IDN")
                    elsif_expr = self.eat_operation()
                    if self.tok.value == "then": self.consume("IDN")

                    elsifevents = ASTListNode("STATEMENTS", [])
                    while self.tok.value not in ["else", "elsif", "end"] and self.tok.type != "EOF":
                        elsifevents.add(self.eat_statement())
                        if self.tok.type == "SMC": self.consume("SMC")
                        elif self.tok.type == "NWL": self.consume("NWL")
                        elif self.tok.type == "EOF": break
                        else: self.eh.construct_error(f"line ended with incorrect character")

                    elsifs.append([elsif_expr, elsifevents])

                if self.tok.value == "end":
                    self.consume("IDN")
                    return ASTListNode("CONDITIONAL", [[if_expr, ifevents], elsifs, elseevents])

            if self.tok.value == "else":
                self.consume("IDN")

                while self.tok.value != "end" and self.tok.type != "EOF":
                    elseevents.add(self.eat_statement())
                    if self.tok.type == "SMC": self.consume("SMC")
                    elif self.tok.type == "NWL": self.consume("NWL")
                    elif self.tok.type == "EOF": break
                    else: self.eh.construct_error(f"line ended with incorrect character")

        self.consume("IDN")
        return ASTListNode("CONDITIONAL", [[if_expr, ifevents], elsifs, elseevents])

    def eat_case_state(self):
        case_expr = self.eat_operation()
        self.consume("NWL")
        cases = []

        while self.tok.value != "end" and self.tok.type != "EOF":
            self.consume("IDN")

            when_expressions = []
            when_events = ASTListNode("STATEMENTS", [])
            while self.tok.type != "NWL":
                when_expressions.append(self.eat_operation())
                if self.tok.type == "COM":
                    self.consume("COM")

            while self.tok.value not in ["end", "when", "else"] and self.tok.type != "EOF":
                when_events.add(self.eat_statement())
                if self.tok.type == "SMC": self.consume("SMC")
                elif self.tok.type == "NWL": self.consume("NWL")
                elif self.tok.type == "EOF": break
                else: self.eh.construct_error(f"line ended with incorrect character")

            cases.append([when_expressions, when_events])

            if self.tok.value == "else":
                break

        else_events = ASTListNode("STATEMENTS", [])
        if self.tok.value == "else":
            self.consume("IDN")

            while self.tok.value not in ["end"] and self.tok.type != "EOF":
                else_events.add(self.eat_statement())
                if self.tok.type == "SMC": self.consume("SMC")
                elif self.tok.type == "NWL": self.consume("NWL")
                elif self.tok.type == "EOF": break
                else: self.eh.construct_error(f"line ended with incorrect character")

        self.consume("IDN")
        return ASTListNode("CASE_WHEN", [case_expr, cases, else_events])

    def eat_statement(self):
        if self.tok.type in ["ADD", "SUB", "NUM", "PRL", "STR"]:
            # self.consume("EQL")
            return self.eat_operation()

        elif self.tok.type == "IDN":
            ctok = self.tok
            self.consume("IDN")

            if self.tok.type == "PRL":
                self.consume("PRL")
                return ASTMultiNode("FUNC_CALL", "fn", ASTDataNode("FUNC_NAME", ctok.value), self.eat_params(look_for = "PRR"))
            elif self.tok.type == "EQL":
                self.consume("EQL")
                return self.eat_variable_assignment(ctok.value)
            elif ctok.value == "def":
                ctok = self.tok
                self.consume("IDN")
                return self.eat_function(ctok.value)
            elif ctok.value == "if":
                return self.eat_conditional()
            elif ctok.value == "unless":
                return self.eat_cond_unless()
            elif ctok.value == "case":
                return self.eat_case_state()
            else:
                return ASTMultiNode("FUNC_CALL", "fn", ASTDataNode("FUNC_NAME", ctok.value), self.eat_params())

        elif self.tok.type == "NWL":
            return ASTDataNode("NONETYPE", None)
        else:
            self.eh.construct_error(f"unrecognized pattern, found {self.tok.type}")

    def construct(self):
        self.eh.reset_pos()
        self.next_tok()

        while self.tok.type != "EOF":
            state = self.eat_statement()
            self.program.add(state)
            if self.tok.type == "SMC": self.consume("SMC")
            elif self.tok.type == "NWL": self.consume("NWL")
            elif self.tok.type == "EOF": break
            else:
                self.eh.construct_error(f"line ended with incorrect character ({self.tok.value})")

        return self.program








# ---------------------------------
# :: INTERPRETER CLASS ::
# ---------------------------------
class Interpreter:
    def __init__(self, ct: Constructor, eh: ErrorHandler, mode: int = 0):
        self.ct = ct
        self.eh = eh
        self.mode = mode
        self.scope = "GLOBAL"
        self.memory = {}
        self.constructed = self.ct.construct()

    def execute(self, show_nodes = False):
        self.eh.reset_pos()
        if show_nodes:
            print(f"\n\033[32m[NODES]\033[0m\n{self.constructed}\
            \n\n\033[32m[EXECUTION]\033[0m\n")
        return self.traverse(self.constructed)

    def trav_obj_funcs(self, value, func):
        match func:
            case "to_s":
                return str(value)
            case "to_i":
                return int(value)
            case "to_f":
                return float(value)
            case "length":
                if isinstance(value, str):
                    return len(value)
                self.eh.interpret_error("cannot get length of non-string object")
            case "_":
                self.eh.interpret_error("unrecognized object function")

    def get_global_variable(self, node):
        if node.value in self.memory:
            if self.memory[node.value][0] == "VAR":
                return self.memory[node.value][1]
            self.eh.interpret_error("name not a variable")
        else:
            self.eh.interpret_error(f"variable [{node.value}] does not exist")

    def comb_comp(self, val1, val2):
        return (val1 > val2) * 1 + (val1 == val2) * 0 + (val1 < val2) * -1

    def get_empty(self, val):
        if isinstance(val, int):
            return 0
        if isinstance(val, float):
            return 0.0
        if isinstance(val, str):
            return ""
        if isinstance(val, bool):
            return False
        return None

    def traverse(self, node):
        self.eh.pos += 1

        if node.type == "STATEMENTS":
            for i, child in enumerate(node.sub_nodes):
                if self.mode == 1:
                    val = self.traverse(child)
                    fin = REPLACEMENTS[val] if val in REPLACEMENTS else val
                    print(f"=> {fin}")
                elif self.mode == 0: self.traverse(child)
            return 1

        if node.type == "OPERATION":
            val1 = self.traverse(node.left)
            val2 = self.traverse(node.right)

            match node.value:
                case "+": return val1 + val2
                case "-": return val1 - val2
                case "*": return val1 * val2
                case "/": return val1 / val2
                case "**": return val1 ** val2
                case "%": return val1 % val2
                case ".": return self.trav_obj_funcs(val1, val2)
                case "==": return val1 == val2
                case "!=": return val1 != val2
                case ">": return val1 > val2
                case "<": return val1 < val2
                case ">=": return val1 >= val2
                case "<=": return val1 <= val2
                case "<=>": return self.comb_comp(val1, val2)
                case "===": return val1 in val2
                case "if": return val1 if val2 else self.get_empty(val1)
                case "unless": return val1 if not val2 else self.get_empty(val1)
                case "&&": return val1 and val2
                case "||": return val1 or val2
                case _: self.eh.interpret_error("unrecognized operator")

        if node.type == "UNARY_OP":
            val = self.traverse(node.right)

            match node.value:
                case "+": return +float(val)
                case "-": return -float(val)
                case "!": return not val
                case _: self.eh.interpret_error("unrecognized unary operation")

        if node.type in ["NUMBER", "BOOLEAN", "FUNC_NAME", "STRING", "VARIABLE_NAME", "NONETYPE"]:
            return node.value

        if node.type == "ASSIGNMENT":
            var_name = self.traverse(node.left)
            val = self.traverse(node.right)
            if self.scope == "GLOBAL" or var_name[0] == "$":
                self.memory[var_name] = ["VAR", val]
            else:
                self.memory[self.scope][3][var_name] = ["VAR", val]
            return val

        if node.type == "VARIABLE":
            if self.scope == "GLOBAL":
                return self.get_global_variable(node)

            if node.value in self.memory[self.scope][3]:
                if self.memory[self.scope][3][node.value][0] == "VAR":
                    return self.memory[self.scope][3][node.value][1]
                self.eh.interpret_error("name not a variable")
            else: return self.get_global_variable(node)

        if node.type == "FUNC_CALL":
            func_name = self.traverse(node.left)
            params = self.traverse(node.right)

            match func_name:
                case "puts":
                    if len(params) < 1:
                        self.eh.interpret_error("not enough arguments to call 'puts' function")
                    print(params[0])
                case _:
                    if func_name in self.memory:
                        if self.memory[func_name][0] == "FUNC":
                            for p, param in enumerate(self.memory[func_name][1]):
                                if len(params) <= p:
                                    self.eh.interpret_error("missing argument for function call")
                                self.memory[func_name][3][param] = ["VAR", params[p]]
                            old_scope = self.scope
                            self.scope = func_name
                            t = self.traverse(self.memory[func_name][2])
                            self.scope = old_scope
                            return t
                        self.eh.interpret_error("name not a function")
                    else:
                        self.eh.interpret_error("function does not exist")

            return None

        if node.type in ["FUNC_PARAMS", "FUNCTION_ARGS"]:
            return [self.traverse(n) for n in node.sub_nodes]

        if node.type == "FUNCTION":
            fn = self.traverse(node.sub_nodes[0])
            self.memory[fn] = ["FUNC", self.traverse(node.sub_nodes[1]), node.sub_nodes[2], {}]
            return ":" + fn

        if node.type == "CONDITIONAL":
            if_cond = self.traverse(node.sub_nodes[0][0])
            if_events = node.sub_nodes[0][1]

            if if_cond:
                self.traverse(if_events)
            else:
                for ops in node.sub_nodes[1]:
                    condition = ops[0]
                    events = ops[1]
                    if self.traverse(condition):
                        self.traverse(events)
                        return None
                self.traverse(node.sub_nodes[2])

            return None

        if node.type == "UNLESS_CONDITIONAL":
            if_cond = self.traverse(node.sub_nodes[0][0])
            if_events = node.sub_nodes[0][1]

            if not if_cond:
                self.traverse(if_events)
            else: self.traverse(node.sub_nodes[1])

            return None

        if node.type == "CASE_WHEN":
            case = self.traverse(node.sub_nodes[0])

            for cases in node.sub_nodes[1]:
                c_expr = [self.traverse(n) for n in cases[0]]
                c_evnts = cases[1]

                if case in c_expr:
                    self.traverse(c_evnts)
                    return None

            self.traverse(node.sub_nodes[2])

            return None

        self.eh.interpret_error(f"unrecognized node is {node.type}")









# ---------------------------------
# :: MAIN ::
# ---------------------------------
def main() -> None:
    out = 1 if "--out" in sys.argv else 0
    show_consumes = 1 if "--shc" in sys.argv else 0
    show_nodes = 1 if "--shn" in sys.argv else 0
    eh = ErrorHandler()

    if len(sys.argv) > 1:
        if path.exists(sys.argv[1]):
            with open(sys.argv[1], "r", encoding = "utf-8") as code_file:
                code = "".join(code_file.readlines())
            t = Tokenizer(code.replace("\\n", "\n"), eh)
            c = Constructor(t, eh, show_consumes)
            i = Interpreter(c, eh, out)
            i.execute(show_nodes)

    else:
        line = 1
        while True:
            user = input(f"\nirb(main):00{line}:0> ")
            if user.strip() == "":
                break
            t = Tokenizer(user + "\n", eh)
            c = Constructor(t, eh)
            i = Interpreter(c, eh, 1)
            i.execute(show_nodes)
            line += 1

if __name__ == "__main__":
    main()
