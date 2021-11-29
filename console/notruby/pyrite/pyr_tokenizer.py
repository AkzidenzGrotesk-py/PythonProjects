'''
Tokenizer class for Pyrite.
'''
from pyr_globals import VALID_CHARS
from pyr_general_classes import Token
from pyr_errorhandler import ErrorHandler

class Tokenizer:
    '''
    Tokenizer class takes in text and an ErrorHandler.
    '''
    def __init__(self, text: str, er_h: ErrorHandler):
        self.text = text
        self.er_h = er_h
        self.cpos = -1
        self.cchar = None
        self.buffer = []

    def advance(self):
        '''Advance forward a character or return the EOF'''
        if self.cpos >= len(self.text) - 1:
            self.cchar = "EOF"
            return

        self.cpos += 1
        self.er_h.pos += 1
        self.cchar = self.text[self.cpos]

    def retreat(self):
        '''Go backwards a character'''
        if self.cpos <= 0:
            return

        self.cpos -= 1
        self.er_h.pos -= 1
        self.cchar = self.text[self.cpos]

    def peek(self) -> str:
        '''Peeks one character forward'''
        if self.cpos + 1 >= len(self.text) - 1:
            return "EOF"
        return self.text[self.cpos + 1]

    def dob_peek(self) -> str:
        '''Peeks two characters forward'''
        if self.cpos + 2 >= len(self.text) - 1:
            return "EOF"
        return self.text[self.cpos + 1] + self.text[self.cpos + 2]

    def collect_number(self):
        '''Collects numbers from text'''
        col = ""
        while (self.cchar.isdigit() or self.cchar == ".") and self.cchar != "EOF":
            if self.cchar == ".":
                if not self.peek().isdigit():
                    break
            col += self.cchar
            self.advance()
        if self.cchar != "EOF":
            self.retreat()
        return float(col) if '.' in col else int(col)

    def collect_identity(self) -> str:
        '''Collects identities from text'''
        col = ""
        while self.cchar in VALID_CHARS and self.cchar != "EOF":
            col += self.cchar
            self.advance()
        if self.cchar != "EOF":
            self.retreat()
        return col

    def collect_string(self, entry = "\"") -> str:
        '''Collect strings from text'''
        col = ""
        self.advance()
        while self.cchar not in [entry, "EOF"]:
            if self.cchar + self.peek() == "#{":
                self.advance()
                self.advance()
                variable = self.collect_identity()
                self.advance()
                if self.cchar == "}":
                    self.advance()
                else: self.er_h.token_error(f"missing closing operator, found {self.cchar}")
                self.buffer.extend([
                    Token("STR", col),
                    Token("ADD", "+"),
                    Token("IDN", variable),
                    Token("DOT", "."),
                    Token("IDN", "to_s"),
                    Token("ADD", "+")
                ])
                col = ""

                if self.cchar == entry:
                    return ""

            col += self.cchar

            if self.cchar == "\n":
                self.er_h.token_error("will not collect string past newline")

            self.advance()
        return col

    def get_token(self, prev = None):
        '''Get next token, repeated calls return more tokens.'''
        if len(self.buffer) > 0:
            return self.buffer.pop(0)

        self.advance()

        while self.cchar in [" ", "\t", "\r"] and self.cchar != "EOF":
            self.advance()

        if self.cchar == "\n":
            return Token("NWL", "\\n")

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
            case '..':
                self.advance()
                return Token("RANGE", "..")

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

        self.er_h.token_error("token not recognized")
