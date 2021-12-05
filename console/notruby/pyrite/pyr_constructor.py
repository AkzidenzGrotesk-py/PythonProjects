'''
Constructor class for Pyrite
'''
from pyr_globals import TOKENS
from pyr_general_classes import Token, ASTDataNode, ASTMultiNode, ASTListNode
from pyr_errorhandler import ErrorHandler
from pyr_tokenizer import Tokenizer

class Constructor:
    '''
    Constructor class takes in a Tokenizer and ErrorHandler and builds an AST.
    '''
    def __init__(self, ti: Tokenizer, eh: ErrorHandler, show_consumes: int = 0):
        self.tokenizer = ti
        self.er_h = eh
        self.show_consumes = show_consumes
        self.ltok = Token("NON", None)
        self.tok = Token("NON", None)
        self.program = ASTListNode("STATEMENTS", [])

        if show_consumes:
            print("\033[32m[CONSUMPTIONS]\033[0m")

    def next_tok(self):
        '''Move to next token.'''
        self.ltok = self.tok
        self.tok = self.tokenizer.get_token(self.ltok)

    def consume(self, _type: str):
        '''Move to next token if correct type is expected.'''
        if self.tok.type == _type:
            if self.show_consumes:
                print(self.tok, end = "")
            self.next_tok()
            self.er_h.pos += 1

        else:
            self.er_h.construct_error(f"token has not been consumed correctly,\
 looking for {_type} ({TOKENS[_type]}) found {self.tok.type} with {self.tok.value}")

    def eat_arrays(self):
        '''Eat arrays'''
        self.consume("SQL")

        array_values = ASTListNode("ARRAY_TYPE", [])
        while self.tok.type not in ["SQR", "EOF"]:
            array_values.add(self.eat_operation())

            if self .tok.type not in ["SQR", "EOF", "SMC"]:
                self.consume("COM")

        self.consume("SQR")

        return array_values

    def eat_array_index(self, var_name: str, depth: int = 0):
        '''Eats array index syntax'''
        self.consume("SQL")
        index = self.eat_factor()
        self.consume("SQR")

        sub_indexes = []
        if self.tok.type == "SQL":
            sub_indexes = self.eat_array_index("", depth + 1)

        if sub_indexes:
            rtrn_val =  [index, *sub_indexes]
        else:
            rtrn_val =  [index]

        if depth > 0:
            return rtrn_val

        return ASTMultiNode("ARRAY_VARIABLE",
        "array",
        var_name, rtrn_val)

    def eat_factor(self):
        '''Eats factor values'''
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
            case "SQL":
                return self.eat_arrays()
            case "STR":
                self.consume("STR")
                return ASTDataNode("STRING", ctok.value)
            case "IDN":
                last_tok = self.ltok
                self.consume("IDN")
                if last_tok.type == "DOT":
                    return ASTDataNode("FUNC_NAME", ctok.value)
                elif self.tok.type == "PRL":
                    self.consume("PRL")
                    call = ASTMultiNode("FUNC_CALL", "fn",
                        ASTDataNode("FUNC_NAME", ctok.value),
                        self.eat_params(look_for = "PRR"))
                    return call
                elif self.tok.type == "SQL":
                    return self.eat_array_index(ctok.value)
                return ASTDataNode("VARIABLE", ctok.value)

        self.er_h.construct_error(
            f"unrecognized symbol is {self.tok.type} when trying to eat factors"
        )

    def eat_power(self):
        '''Eat powers and dot operations'''
        node = self.eat_factor()

        while self.tok.type in ["POW", "DOT"]:
            ctok = self.tok
            if ctok.type == "POW":
                self.consume("POW")
            elif ctok.type == "DOT":
                self.consume("DOT")
            else: self.er_h.construct_error("unrecognized symbol when trying to eat powers")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_factor())

        return node

    def eat_term(self):
        '''Eat terms'''
        node = self.eat_power()

        while self.tok.type in ["MUL", "DIV", "PER"]:
            ctok = self.tok
            if ctok.type == "MUL":
                self.consume("MUL")
            elif ctok.type == "DIV":
                self.consume("DIV")
            elif ctok.type == "PER":
                self.consume("PER")
            else: self.er_h.construct_error("unrecognized symbol when trying to eat terms")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_power())

        return node

    def eat_expression(self):
        '''Eats expressions'''
        node = self.eat_term()

        while self.tok.type in ["ADD", "SUB"]:
            ctok = self.tok
            if ctok.type == "ADD":
                self.consume("ADD")
            elif ctok.type == "SUB":
                self.consume("SUB")
            else: self.er_h.construct_error("unrecognized symbol when trying to eat expression")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_term())

        return node

    def eat_equalities(self):
        '''Eats equalities'''
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
            else: self.er_h.construct_error("unrecognized symbol when trying to eat equality")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_expression())

        return node

    def eat_andornot(self):
        '''Eats && || ! operators'''
        node = self.eat_equalities()

        while self.tok.type in ["AND", "NOT", "ORO"]:
            ctok = self.tok
            if ctok.type == "AND":
                self.consume("AND")
            elif ctok.type == "ORO":
                self.consume("ORO")
            else: self.er_h.construct_error("unrecognized symbol when trying to eat AND OR NOT")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_equalities())

        return node

    def eat_inlines(self):
        '''Eats inline if/unless calls'''
        node = self.eat_andornot()

        while self.tok.type in ["IDN", "RANGE"] and self.tok.value in ["if", "unless", ".."]:
            ctok = self.tok
            if ctok.type == "IDN":
                self.consume("IDN")
            elif ctok.type == "RANGE":
                self.consume("RANGE")
            else: self.er_h.construct_error("unrecognized symbol in inlines")

            node = ASTMultiNode("OPERATION", ctok.value, node, self.eat_andornot())

        return node

    def eat_operation(self):
        '''Eats operation'''
        return self.eat_inlines()

    def eat_params(self, look_for = "NWL"):
        '''Eat parameters of function'''
        node = ASTListNode("FUNC_PARAMS", [])
        while self.tok.type not in [look_for, "EOF"]:
            # add argument = value syntax
            node.add(self.eat_operation())

            if self.tok.type not in [look_for, "EOF", "SMC"]:
                self.consume("COM")
        if look_for not in ["NWL", "EOF"]:
            self.consume(look_for)

        return node

    def eat_variable_assignment(self, var_name):
        '''Eat variable assignments'''
        return ASTMultiNode("ASSIGNMENT", "=",
            ASTDataNode("VARIABLE_NAME", var_name),
            self.eat_operation())

    def eat_function(self, func_name):
        '''Eat functions'''
        f_params = ASTListNode("FUNCTION_ARGS", [])

        if self.tok.type == "PRL":
            self.consume("PRL")

            while self.tok.type not in ["PRR", "EOF"]:
                ctok = self.tok
                var_args = False
                if self.tok.type == "MUL":
                    self.consume("MUL")
                    var_args = True
                if self.tok.type == "IDN":
                    ctok = self.tok
                    self.consume("IDN")
                    default_val = None
                    if self.tok.type == "EQL":
                        self.consume("EQL")
                        default_val = self.eat_operation()
                    f_params.add(ASTListNode("FUNCTION_ARGS_EXT",
                    [ASTDataNode("VARIABLE_NAME", ctok.value), default_val, var_args]))

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
                while self.tok.type == "NWL":
                    self.consume("NWL")
            elif self.tok.type == "EOF":
                break
            else:
                self.er_h.construct_error(f"line ended with incorrect character ({self.tok.value})")

        self.consume("IDN")

        return ASTListNode("FUNCTION", [ASTDataNode("FUNC_NAME", func_name), f_params, acts])
        #return ASTMultiNode("FUNCTION", "fn", ASTDataNode("FUNC_NAME", func_name), acts)

    def eat_cond_unless(self):
        '''Eat unless conditions'''
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
            else:
                self.er_h.construct_error("line ended with incorrect character")

        if self.tok.value == "end":
            self.consume("IDN")
            return ASTListNode("UNLESS_CONDITIONAL", [[if_expr, ifevents], elseevents])

        if self.tok.value == "else":
            self.consume("IDN")

            while self.tok.value != "end" and self.tok.type != "EOF":
                elseevents.add(self.eat_statement())
                if self.tok.type == "SMC":
                    self.consume("SMC")
                elif self.tok.type == "NWL":
                    self.consume("NWL")
                elif self.tok.type == "EOF":
                    break
                else: self.er_h.construct_error("line ended with incorrect character")

        self.consume("IDN")
        return ASTListNode("UNLESS_CONDITIONAL", [[if_expr, ifevents], elseevents])

    def eat_conditional(self):
        '''Eat conditional statements'''
        if_expr = self.eat_operation()
        if self.tok.value == "then":
            self.consume("IDN")
        ifevents = ASTListNode("STATEMENTS", [])
        elseevents = ASTListNode("STATEMENTS", [])
        elsifs = []

        while self.tok.value != "end" and self.tok.type != "EOF":
            while self.tok.value not in ["else", "elsif", "end"] and self.tok.type != "EOF":
                ifevents.add(self.eat_statement())
                if self.tok.type == "SMC":
                    self.consume("SMC")
                elif self.tok.type == "NWL":
                    self.consume("NWL")
                elif self.tok.type == "EOF":
                    break
                else: self.er_h.construct_error("line ended with incorrect character")

            if self.tok.value == "end":
                self.consume("IDN")
                return ASTListNode("CONDITIONAL", [[if_expr, ifevents], elsifs, elseevents])

            if self.tok.value == "elsif":
                while self.tok.value not in ["else", "end"] and self.tok.type != "EOF":
                    self.consume("IDN")
                    elsif_expr = self.eat_operation()
                    if self.tok.value == "then":
                        self.consume("IDN")

                    elsifevents = ASTListNode("STATEMENTS", [])
                    while self.tok.value not in ["else", "elsif", "end"] and self.tok.type != "EOF":
                        elsifevents.add(self.eat_statement())
                        if self.tok.type == "SMC":
                            self.consume("SMC")
                        elif self.tok.type == "NWL":
                            self.consume("NWL")
                        elif self.tok.type == "EOF":
                            break
                        else:
                            self.er_h.construct_error("line ended with incorrect character")

                    elsifs.append([elsif_expr, elsifevents])

                if self.tok.value == "end":
                    self.consume("IDN")
                    return ASTListNode("CONDITIONAL", [[if_expr, ifevents], elsifs, elseevents])

            if self.tok.value == "else":
                self.consume("IDN")

                while self.tok.value != "end" and self.tok.type != "EOF":
                    elseevents.add(self.eat_statement())
                    if self.tok.type == "SMC":
                        self.consume("SMC")
                    elif self.tok.type == "NWL":
                        self.consume("NWL")
                    elif self.tok.type == "EOF":
                        break
                    else: self.er_h.construct_error("line ended with incorrect character")

        self.consume("IDN")
        return ASTListNode("CONDITIONAL", [[if_expr, ifevents], elsifs, elseevents])

    def eat_case_state(self):
        '''Eat case/when conditionals'''
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
                if self.tok.type == "SMC":
                    self.consume("SMC")
                elif self.tok.type == "NWL":
                    self.consume("NWL")
                elif self.tok.type == "EOF":
                    break
                else: self.er_h.construct_error("line ended with incorrect character")

            cases.append([when_expressions, when_events])

            if self.tok.value == "else":
                break

        else_events = ASTListNode("STATEMENTS", [])
        if self.tok.value == "else":
            self.consume("IDN")

            while self.tok.value not in ["end"] and self.tok.type != "EOF":
                else_events.add(self.eat_statement())
                if self.tok.type == "SMC":
                    self.consume("SMC")
                elif self.tok.type == "NWL":
                    self.consume("NWL")
                elif self.tok.type == "EOF":
                    break
                else: self.er_h.construct_error("line ended with incorrect character")

        self.consume("IDN")
        return ASTListNode("CASE_WHEN", [case_expr, cases, else_events])

    def eat_while_loop(self, while_type = "forward"):
        '''Eats while, do loops'''

        if while_type in ["forward", "until"]:
            while_expr = self.eat_operation()
            if self.tok.value == "do":
                self.consume("IDN")

        self.consume("NWL")

        while_events = ASTListNode("STATEMENTS", [])
        while self.tok.value != "end" and self.tok.type != "EOF":
            while_events.add(self.eat_statement())
            if self.tok.type == "SMC":
                self.consume("SMC")
            elif self.tok.type == "NWL":
                self.consume("NWL")
            elif self.tok.type == "EOF":
                break
            else: self.er_h.construct_error("line ended with incorrect character")

        self.consume("IDN")

        if while_type == "backwards":
            if self.tok.value == "until":
                while_type = "until"

            self.consume("IDN")
            while_expr = self.eat_operation()

        if while_type in ["backwards", "forward"]:
            return ASTListNode("WHILE_DO", [while_expr, while_events])
        return ASTListNode("UNTIL_DO", [while_expr, while_events])

    def eat_for_loop(self):
        '''Eats for ... in ... loops'''
        v_expands = ASTListNode("FOR_LOOP_VARS", [])

        while self.tok.type != "EOF" and self.tok.value != "in":
            ctok = self.tok
            if self.tok.type == "IDN":
                self.consume("IDN")
                v_expands.add(ASTDataNode("VARIABLE_NAME", ctok.value))
            if self.tok.type != "EOF" and self.tok.value != "in":
                self.consume("COM")
        self.consume("IDN")

        v_expr = self.eat_operation()

        if self.tok.value == "do":
            self.consume("IDN")
        self.consume("NWL")

        for_events = ASTListNode("STATEMENTS", [])
        while self.tok.value != "end" and self.tok.type != "EOF":
            for_events.add(self.eat_statement())
            if self.tok.type == "SMC":
                self.consume("SMC")
            elif self.tok.type == "NWL":
                self.consume("NWL")
            elif self.tok.type == "EOF":
                break
            else: self.er_h.construct_error("line ended with incorrect character")

        self.consume("IDN")
        return ASTListNode("FOR_LOOP", [v_expands, v_expr, for_events])

    def eat_func_return(self):
        '''Eat return statements'''
        rtrn_statement = self.eat_operation()
        return ASTDataNode("RETURN", rtrn_statement)

    def eat_alias(self):
        '''Eat alias statements'''
        ctok = self.tok
        if self.tok.type == "IDN":
            self.consume("IDN")
            alias = ASTDataNode("VARIABLE_NAME", ctok.value)
            ctok = self.tok
            if self.tok.type == "IDN":
                self.consume("IDN")
                original = ASTDataNode("VARIABLE_NAME", ctok.value)

                return ASTMultiNode("NAME_ALIAS", "alias", alias, original)

        self.er_h.construct_error("alias statement missing identifier(s)")

    def eat_undef(self):
        '''Eat undefinitions'''
        ctok = self.tok
        if self.tok.type == "IDN":
            self.consume("IDN")
            return ASTDataNode("UNDEF", ASTDataNode("VARIABLE_NAME", ctok.value))

        self.er_h.construct_error("undef statement missing identifier")

    def eat_block(self, name):
        '''Eats blocks'''
        block_args = ASTListNode("BLOCK_ARGS", [])
        if self.tok.type == "PIP":
            self.consume("PIP")
            while self.tok.type not in ["PIP", "EOF"]:
                ctok = self.tok
                if self.tok.type == "IDN":
                    self.consume("IDN")
                    block_args.add(ASTDataNode("VARIABLE_NAME", ctok.value))
                if self.tok.type == "PIP":
                    break
                if self.tok.type == "COM":
                    self.consume("COM")
                if self.tok.type not in ["IDN", "COM", "PIP"]:
                    self.er_h.construct_error(f"unexpected symbol {self.tok.type} in block arguments")
            self.consume("PIP")

        if self.tok.type == "NWL":
            self.consume("NWL")

        acts = ASTListNode("STATEMENTS", [])
        while self.tok.type not in ["CUR", "EOF"]:
            acts.add(self.eat_statement())

            if self.tok.type != "CUR":
                if self.tok.type == "SMC":
                    self.consume("SMC")
                elif self.tok.type == "NWL":
                    while self.tok.type == "NWL":
                        self.consume("NWL")
                elif self.tok.type == "EOF":
                    break
                else:
                    self.er_h.construct_error(f"line ended with incorrect character ({self.tok.value})")

        self.consume("CUR")

        return ASTListNode("BLOCK_STATE", [ASTDataNode("BLOCK_NAME", name), block_args, acts])

    def eat_yield_call(self):
        '''Eats yields to blocks'''
        args = ASTListNode("YIELD_ARGS", [])
        while self.tok.type not in ["SMC", "NWL", "EOF"]:
            args.add(self.eat_operation())
            if self.tok.type == "COM":
                self.consume("COM")
            elif self.tok.type not in ["SMC", "NWL"]:
                self.er_h.construct_error(f"unrecognized pattern in yield arguments, found {self.tok.type}")

        return ASTMultiNode("YIELD_CALL", "yield", None, args)

    def eat_statement(self):
        '''Eat statements'''
        if self.tok.type in ["ADD", "SUB", "NUM", "PRL", "STR"]:
            return self.eat_operation()

        if self.tok.type == "IDN":
            ctok = self.tok
            self.consume("IDN")

            match ctok.value:
                case "def":
                    ctok = self.tok
                    self.consume("IDN")
                    return self.eat_function(ctok.value)
                case "if":
                    return self.eat_conditional()
                case "unless":
                    return self.eat_cond_unless()
                case "case":
                    return self.eat_case_state()
                case "while":
                    return self.eat_while_loop(while_type = "forward")
                case "begin":
                    return self.eat_while_loop(while_type = "backwards")
                case "until":
                    return self.eat_while_loop(while_type = "until")
                case "break"|"next"|"redo"|"retry":
                    return ASTDataNode("KNOWN_CALL", ctok.value)
                case "for":
                    return self.eat_for_loop()
                case "return":
                    return self.eat_func_return()
                case "alias":
                    return self.eat_alias()
                case "undef":
                    return self.eat_undef()
                case "yield":
                    return self.eat_yield_call()

            match self.tok.type:
                case "PRL":
                    self.consume("PRL")
                    return ASTMultiNode("FUNC_CALL", "fn",
                        ASTDataNode("FUNC_NAME", ctok.value),
                        self.eat_params(look_for = "PRR"))
                case "CUL":
                    self.consume("CUL")
                    return self.eat_block(ctok.value)
                case "EQL":
                    self.consume("EQL")
                    return self.eat_variable_assignment(ctok.value)

            return ASTMultiNode("FUNC_CALL", "fn",
                ASTDataNode("FUNC_NAME", ctok.value),
                self.eat_params())

        if self.tok.type == "NWL":
            return ASTDataNode("NONETYPE", None)

        self.er_h.construct_error(f"unrecognized pattern, found {self.tok.type}")

    def construct(self) -> ASTListNode:
        '''Construct an entire tree'''
        self.er_h.reset_pos()
        self.next_tok()

        while self.tok.type != "EOF":
            state = self.eat_statement()
            self.program.add(state)
            if self.tok.type == "SMC":
                self.consume("SMC")
            elif self.tok.type == "NWL":
                self.consume("NWL")
            elif self.tok.type == "EOF":
                break
            else:
                self.er_h.construct_error(f"line ended with incorrect character ({self.tok.value})")

        return self.program
