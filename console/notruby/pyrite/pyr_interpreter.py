'''
Interpreter class for Pyrite.
'''

from pyr_globals import REPLACEMENTS, BREAK_OPERATIONS
from pyr_general_classes import RubyRange, ASTDataNode, ASTListNode, ASTMultiNode
from pyr_errorhandler import ErrorHandler
from pyr_constructor import Constructor

class Interpreter:
    '''
    Interpreter class traverses abstract syntax trees and executes them.
    '''
    def __init__(self, ct: Constructor, eh: ErrorHandler, mode: int = 0, show_memory: int = 0):
        self.constructor = ct
        self.er_h = eh
        self.mode = mode
        self.show_mem = show_memory
        self.scope = "GLOBAL"
        self.memory = {
            "TEMP_FOR" : ["SUBMEM", {}],
            "TEMP_RETURN" : ["TEMPMEM", None]
        }
        self.active_mem = []
        self.constructed = self.constructor.construct()

    def execute(self, show_nodes = False):
        '''Begins execution and traversal of tree.'''
        self.er_h.reset_pos()
        if show_nodes:
            print(f"\n\033[32m[NODES]\033[0m\n{self.constructed}\
\n\n\033[32m[EXECUTION]\033[0m")
        vtr = self.traverse(self.constructed)
        if self.show_mem:
            print(self.memory)
        return vtr

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
                if isinstance(value, (str, list, tuple)):
                    return len(value)
                self.er_h.interpret_error("cannot get length of non-string object")
            case "capitalize":
                if isinstance(value, str):
                    return value.capitalize()
                self.er_h.interpret_error("cannot capitalize non-string object")
            case "upcase":
                if isinstance(value, str):
                    return value.upper()
                self.er_h.interpret_error("cannot upcase non-string object")
            case "donwcase":
                if isinstance(value, str):
                    return value.lower()
                self.er_h.interpret_error("cannot downcase non-string object")
            case "lstrip":
                if isinstance(value, str):
                    return value.lstrip()
                self.er_h.interpret_error("cannot strip leading whitespace of non-string object")
            case "rstrip":
                if isinstance(value, str):
                    return value.rstrip()
                self.er_h.interpret_error("cannot strip trailing whitespace of non-string object")
            case "strip":
                if isinstance(value, str):
                    return value.strip()
                self.er_h.interpret_error("cannot strip whitespace of non-string object")
            case "_":
                self.er_h.interpret_error("unrecognized object function")

    def get_list_item_at_index(self, item, indexes):
        '''With list `item` and list of `indexes`,
        gets item[indexes[0]][indexes[1]][indexes[2]]...th item'''
        if len(indexes) == 1:
            return item[self.traverse(indexes[0])]
        if len(indexes) > 1:
            return self.get_list_item_at_index(item[self.traverse(indexes[0])], indexes[1:])

        return item

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

    def get_global_array_var(self, node):
        '''Get global variables'''
        if node.left in self.memory:
            if self.memory[node.left][0] == "VAR":
                return self.get_list_item_at_index(self.memory[node.left][1], node.right)
            self.er_h.interpret_error("name not a variable")
        else:
            for mems in list(dict.fromkeys(self.active_mem)):
                if node.left in self.memory[mems][1]:
                    if self.memory[mems][1][node.left][0] == "VAR":
                        return self.get_list_item_at_index(self.memory[mems][1][node.left][1],
                        node.right)
                    self.er_h.interpret_error("name not a variable")

            self.er_h.interpret_error(f"variable [{node.left}] does not exist")


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

    def traverse(self, node, statement_start: int = 0):
        '''Traverses nodes.'''

        # if self.show_mem:
        #    print(self.memory)

        self.er_h.pos += 1

        if node.type == "STATEMENTS":
            rtrn_value = 1
            for node_count, child in enumerate(node.sub_nodes[statement_start:]):
                if self.mode == 1:
                    val = self.traverse(child)
                    fin = REPLACEMENTS[val] if val in REPLACEMENTS else val
                    print(f"=> {fin}")
                elif self.mode == 0:
                    trav_result = self.traverse(child)
                    if trav_result in BREAK_OPERATIONS:
                        rtrn_value = trav_result
                        break
                    if isinstance(trav_result, list):
                        if trav_result[0] in BREAK_OPERATIONS:
                            trav_result.append(statement_start + node_count + 1)
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
            "STRING", "VARIABLE_NAME", "NONETYPE", "KNOWN_CALL",
            "BLOCK_NAME"
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

        if node.type == "ARRAY_VARIABLE":
            if self.scope == "GLOBAL":
                return self.get_global_array_var(node)

            if node.left in self.memory[self.scope][3]:
                if self.memory[self.scope][3][node.left][0] == "VAR":
                    return self.get_list_item_at_index(self.memory[self.scope][3][node.left][1],
                    node.right)
                self.er_h.interpret_error("name not a variable")
            else: return self.get_global_array_var(node)

        if node.type == "FUNC_CALL":
            func_name = self.traverse(node.left)
            params = self.traverse(node.right)

            match func_name:
                case "puts":
                    if len(params) < 1:
                        self.er_h.interpret_error("not enough arguments to call 'puts' function")

                    if isinstance(params[0], list):
                        print("\n".join([str(i) for i in params[0]]))
                    else:
                        print(params[0])
                case "print":
                    if len(params) < 1:
                        self.er_h.interpret_error("not enough arguments to call 'puts' function")
                    print(params[0], end = "")
                case _:
                    if func_name in self.memory:
                        if self.memory[func_name][0] == "FUNC":
                            for p, [param,
                                default_val,
                                is_variable] in enumerate(self.memory[func_name][1]):
                                #if len(params) <= p:
                                #    self.er_h.interpret_error("missing argument for function call")
                                if is_variable:
                                    self.memory[func_name][3][param] = ["VAR", params[p:]]
                                    break

                                if default_val is None:
                                    self.memory[func_name][3][param] = ["VAR", params[p]]
                                else:
                                    if p > len(params) - 1:
                                        self.memory[func_name][3][param] = ["VAR", default_val]
                                    else:
                                        self.memory[func_name][3][param] = ["VAR", params[p]]
                            old_scope = self.scope
                            self.scope = func_name
                            trav = self.traverse(self.memory[func_name][2])
                            while trav is not None:
                                if isinstance(trav, list):
                                    for p, param in enumerate(self.memory[func_name][4][1]):
                                        if len(trav[1:-1]) <= p:
                                           self.er_h.interpret_error("missing argument for function call")
                                        self.memory[func_name][3][param] = ["VAR", (trav[1:-1])[p]]
                                    self.traverse(self.memory[func_name][4][2])
                                    trav = self.traverse(self.memory[func_name][2], trav[-1])
                                else:
                                    break
                            self.scope = old_scope
                            return self.memory["TEMP_RETURN"][1] if trav == "return" else None
                        self.er_h.interpret_error("name not a function")
                    else:
                        self.er_h.interpret_error("function does not exist")

            return None

        # if node.type == "FUNCTION_ARGS":
        #     return [self.traverse(n) for n in node.sub_nodes]

        if node.type == "FUNCTION_ARGS_EXT":
            return [
                self.traverse(node.sub_nodes[0]),
                self.traverse(node.sub_nodes[1]) if node.sub_nodes[1] is not None else None,
                node.sub_nodes[2]
            ]

        if node.type in ["FUNC_PARAMS", "FOR_LOOP_VARS",
                "FUNCTION_ARGS", "ARRAY_TYPE", "BLOCK_ARGS",
                "YIELD_ARGS"]:
            return [self.traverse(n) for n in node.sub_nodes]

        if node.type == "FUNCTION":
            func_name = self.traverse(node.sub_nodes[0])
            self.memory[func_name] = [
                "FUNC",
                self.traverse(node.sub_nodes[1]),
                node.sub_nodes[2], {},
                []
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

        if node.type == "RETURN":
            self.memory["TEMP_RETURN"][1] = self.traverse(node.value)
            return "return"

        if node.type == "NAME_ALIAS":
            alias_name = self.traverse(node.left)
            alias_of = self.traverse(node.right)

            if alias_of in self.memory:
                if self.memory[alias_of][0] == "FUNC":
                    self.memory[alias_name] = [self.memory[alias_of][0], self.memory[alias_of][1],
                                               self.memory[alias_of][2], self.memory[alias_of][3]]
                    return None

            if self.scope == "GLOBAL" or var_name[0] == "$":
                self.memory[alias_name] = [self.memory[alias_of][0], self.memory[alias_of][1]]
            else:
                self.memory[self.scope][3][alias_name] = [self.memory[self.scope][3][alias_of][0],
                                                          self.memory[self.scope][3][alias_of][1]]
            return None

        if node.type == "UNDEF":
            to_undef = self.traverse(node.value)
            if to_undef in self.memory:
                del self.memory[to_undef]
            elif to_undef in self.memory[self.scope][3]:
                del self.memory[self.scope][3][to_undef]
            else:
                self.er_h.interpreter(f"cannot undefine '{to_undef}'")
            return None

        if node.type == "BLOCK_STATE":
            block_name = self.traverse(node.sub_nodes[0])
            block_args = self.traverse(node.sub_nodes[1])

            self.memory[block_name][4] = [
                "BLOCK",
                block_args,
                node.sub_nodes[2]
            ]
            self.traverse(ASTMultiNode("FUNC_CALL", "fn",
                ASTDataNode("FUNC_NAME", block_name),
                ASTListNode("FUNC_PARAMS", [])))
            # self.traverse(self.memory[block_name][4][2])
            return None

        if node.type == "YIELD_CALL":
            arguments = self.traverse(node.right)

            return ["yield", *arguments]

        self.er_h.interpret_error(f"unrecognized node is {node.type}")
