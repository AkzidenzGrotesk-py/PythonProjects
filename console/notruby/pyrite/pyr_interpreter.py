'''
Interpreter class for Pyrite.
'''

from pyr_globals import REPLACEMENTS, BREAK_OPERATIONS
from pyr_general_classes import RubyRange
from pyr_errorhandler import ErrorHandler
from pyr_constructor import Constructor


class Interpreter:
    '''
    Interpreter class traverses abstract syntax trees and executes them.
    '''
    def __init__(self, ct: Constructor, eh: ErrorHandler, mode: int = 0):
        self.constructor = ct
        self.er_h = eh
        self.mode = mode
        self.scope = "GLOBAL"
        self.memory = {
            "TEMP_FOR" : ["SUBMEM", {}]
        }
        self.active_mem = []
        self.constructed = self.constructor.construct()

    def execute(self, show_nodes = False):
        '''Begins execution and traversal of tree.'''
        self.er_h.reset_pos()
        if show_nodes:
            print(f"\n\033[32m[NODES]\033[0m\n{self.constructed}\
\n\n\033[32m[EXECUTION]\033[0m")
        return self.traverse(self.constructed)

    def trav_obj_funcs(self, value, func):
        '''Traverse functions of objects/dot operations'''
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
                self.er_h.interpret_error("cannot get length of non-string object")
            case "_":
                self.er_h.interpret_error("unrecognized object function")

    def get_global_variable(self, node):
        '''Get global variables'''
        if node.value in self.memory:
            if self.memory[node.value][0] == "VAR":
                return self.memory[node.value][1]
            self.er_h.interpret_error("name not a variable")
        else:
            for mems in list(dict.fromkeys(self.active_mem)):
                if node.value in self.memory[mems][1]:
                    if self.memory[mems][1][node.value][0] == "VAR":
                        return self.memory[mems][1][node.value][1]
                    self.er_h.interpret_error("name not a variable")

            self.er_h.interpret_error(f"variable [{node.value}] does not exist")

    @staticmethod
    def comb_comp(val1, val2):
        '''Does a ruby <=> comparison'''
        return (val1 > val2) * 1 + (val1 == val2) * 0 + (val1 < val2) * -1

    @staticmethod
    def get_empty(val):
        '''Gets the empty type for valid types'''
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
        '''Traverses nodes.'''
        self.er_h.pos += 1

        if node.type == "STATEMENTS":
            rtrn_value = 1
            for child in node.sub_nodes:
                if self.mode == 1:
                    val = self.traverse(child)
                    fin = REPLACEMENTS[val] if val in REPLACEMENTS else val
                    print(f"=> {fin}")
                elif self.mode == 0:
                    trav_result = self.traverse(child)
                    if trav_result in BREAK_OPERATIONS:
                        rtrn_value = trav_result
                        break
            return rtrn_value

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
                case "..": return RubyRange(val1, val2 + 1)
                case _: self.er_h.interpret_error("unrecognized operator")

        if node.type == "UNARY_OP":
            val = self.traverse(node.right)

            match node.value:
                case "+": return +float(val)
                case "-": return -float(val)
                case "!": return not val
                case _: self.er_h.interpret_error("unrecognized unary operation")

        if node.type in [
            "NUMBER", "BOOLEAN", "FUNC_NAME",
            "STRING", "VARIABLE_NAME", "NONETYPE", "KNOWN_CALL"
             ]:
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
                self.er_h.interpret_error("name not a variable")
            else: return self.get_global_variable(node)

        if node.type == "FUNC_CALL":
            func_name = self.traverse(node.left)
            params = self.traverse(node.right)

            match func_name:
                case "puts":
                    if len(params) < 1:
                        self.er_h.interpret_error("not enough arguments to call 'puts' function")
                    print(params[0])
                case _:
                    if func_name in self.memory:
                        if self.memory[func_name][0] == "FUNC":
                            for p, param in enumerate(self.memory[func_name][1]):
                                if len(params) <= p:
                                    self.er_h.interpret_error("missing argument for function call")
                                self.memory[func_name][3][param] = ["VAR", params[p]]
                            old_scope = self.scope
                            self.scope = func_name
                            trav = self.traverse(self.memory[func_name][2])
                            self.scope = old_scope
                            return trav
                        self.er_h.interpret_error("name not a function")
                    else:
                        self.er_h.interpret_error("function does not exist")

            return None

        if node.type in ["FUNC_PARAMS", "FUNCTION_ARGS", "FOR_LOOP_VARS"]:
            return [self.traverse(n) for n in node.sub_nodes]

        if node.type == "FUNCTION":
            func_name = self.traverse(node.sub_nodes[0])
            self.memory[func_name] = [
                "FUNC",
                self.traverse(node.sub_nodes[1]),
                node.sub_nodes[2], {}
            ]
            return ":" + func_name

        if node.type == "CONDITIONAL":
            if_cond = self.traverse(node.sub_nodes[0][0])
            if_events = node.sub_nodes[0][1]

            if if_cond:
                return self.traverse(if_events)
            else:
                for ops in node.sub_nodes[1]:
                    condition = ops[0]
                    events = ops[1]
                    if self.traverse(condition):
                        return self.traverse(events)
                return self.traverse(node.sub_nodes[2])

        if node.type == "UNLESS_CONDITIONAL":
            if_cond = self.traverse(node.sub_nodes[0][0])
            if_events = node.sub_nodes[0][1]

            if not if_cond:
                return self.traverse(if_events)
            return self.traverse(node.sub_nodes[1])


        if node.type == "CASE_WHEN":
            case = self.traverse(node.sub_nodes[0])

            for cases in node.sub_nodes[1]:
                c_expr = [self.traverse(n) for n in cases[0]]
                c_evnts = cases[1]

                for ind_case in c_expr:
                    if isinstance(ind_case, RubyRange):
                        if case in ind_case.get_range():
                            return self.traverse(c_evnts)


                    else:
                        if case in ind_case:
                            return  self.traverse(c_evnts)

            self.traverse(node.sub_nodes[2])

            return None

        if node.type == "WHILE_DO":
            while self.traverse(node.sub_nodes[0]):
                trav_result = self.traverse(node.sub_nodes[1])
                if trav_result == "next":
                    continue
                if trav_result == "break":
                    break
                if trav_result == "retry":
                    self.traverse(node)
                if trav_result == "redo":
                    self.er_h.interpret_warning("redo command not supported.")

            return None

        if node.type == "UNTIL_DO":
            while not self.traverse(node.sub_nodes[0]):
                trav_result = self.traverse(node.sub_nodes[1])
                if trav_result == "next":
                    continue
                if trav_result == "break":
                    break
                if trav_result == "retry":
                    self.traverse(node)
                if trav_result == "redo":
                    self.er_h.interpret_warning("redo command not supported.")

            return None

        if node.type == "FOR_LOOP":
            expand_to = self.traverse(node.sub_nodes[0])
            loop_over = self.traverse(node.sub_nodes[1])
            if isinstance(loop_over, RubyRange):
                loop_over = loop_over.get_range()

            self.active_mem.append("TEMP_FOR")

            for values in loop_over:
                for i, expand in enumerate(expand_to):
                    if isinstance(values, (str, list, tuple)):
                        self.memory["TEMP_FOR"][1][expand] = ["VAR", values[i]]
                    else:
                        self.memory["TEMP_FOR"][1][expand] = ["VAR", values]

                trav_result = self.traverse(node.sub_nodes[2])
                if trav_result == "next":
                    continue
                if trav_result == "break":
                    break
                if trav_result == "retry":
                    self.traverse(node)
                if trav_result == "redo":
                    self.er_h.interpret_warning("redo command not supported.")

            self.active_mem.remove("TEMP_FOR")
            return None

        self.er_h.interpret_error(f"unrecognized node is {node.type}")
