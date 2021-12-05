'''
Global variables for Pyrite.
'''

from string import ascii_letters, digits as ascii_digits

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
    "BOOL" : False,
    "RANGE" : "..",
    "SQL" : "[",
    "SQR" : "]",
    "CUL" : "{",
    "CUR" : "}",
    "PIP" : "|",
}
VALID_CHARS = ascii_letters + ascii_digits + "_$"
REPLACEMENTS = {
    True : "true",
    False : "false",
    None : "nil"
}
NOADD_TYPES = ["NONETYPE"]
BREAK_OPERATIONS = ["break", "next", "redo", "retry", "return", "yield"]
