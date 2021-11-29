'''
General classes for Pyrite.
'''

from pyr_globals import NOADD_TYPES

# TOKENS
class Token:
    '''
    Token(type [TOKENS], value)
    Passed from Tokenizer -> Constructor
    '''
    def __init__(self, _type: str, value):
        self.type = _type
        self.value = value

    def __repr__(self):
        return f"(\033[33m{self.type}\033[0m, {self.value}) " +\
            ("\n" if self.value == "\\n" else "")

    def __str__(self):
        return self.__repr__()

# ASTDATANODE
class ASTDataNode:
    '''
    ASTDataNode(type, value)
    Used to construct ASTs and hold individual pieces of data.
    '''
    def __init__(self, _type: str, value):
        self.type = _type
        self.value = value

    def __repr__(self):
        return f"(\033[33m{self.type}\033[0m, {self.value})"

    def __str__(self):
        return self.__repr__()

# ASTMULTINODE
class ASTMultiNode:
    '''
    ASTMultiNode(type, value, left, right)
    Used to construct ASTs and hold operations with left and right sides.
    '''
    def __init__(self, _type: str, value: str, left: ASTDataNode, right: ASTDataNode):
        self.type = _type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"(\033[33m{self.type}\033[0m, {self.value},\
 {self.left.__repr__()}, {self.right.__repr__()})"

    def __str__(self):
        return self.__repr__()

# ASTLISTNODE
class ASTListNode:
    '''
    ASTListNode(type, sub_nodes)
    Used to construct ASTs and hold lists of subnodes.
    '''
    def __init__(self, _type: str, sub_nodes):
        self.type = _type
        self.sub_nodes = sub_nodes

    def add(self, new_node):
        '''Add a new node to sub_nodes'''
        if new_node.type not in NOADD_TYPES:
            self.sub_nodes.append(new_node)

    def __repr__(self):
        sns = ",\n\t".join([sn.__repr__() for sn in self.sub_nodes])
        return f"(\033[33m{self.type}\033[0m,\n\t{sns}\n\t)"

    def __str__(self):
        return self.__repr__()

# RANGE
class RubyRange:
    '''
    A modification of the range() object to support ruby.
    '''
    def __init__(self, _min = 0, _max = 0):
        self.min = _min
        self.max = _max

    def get_range(self):
        '''Returns range object'''
        return range(self.min, self.max)

    def __repr__(self):
        return f"{self.min}..{self.max - 1}"

    def __str__(self):
        return self.__repr__()
