'''
Main file for Pyrite.
'''

from sys import argv
from os import path
from pyr_errorhandler import ErrorHandler
from pyr_tokenizer import Tokenizer
from pyr_constructor import Constructor
from pyr_interpreter import Interpreter

def main() -> None:
    '''Main call for Pyrite'''
    out = 1 if "--out" in argv else 0
    show_consumes = 1 if "--shc" in argv else 0
    show_nodes = 1 if "--shn" in argv else 0
    er_h = ErrorHandler()

    if len(argv) > 1:
        if path.exists(argv[1]):
            with open(argv[1], "r", encoding = "utf-8") as code_file:
                code = "".join(code_file.readlines())
            tok = Tokenizer(code.replace("\\n", "\n"), er_h)
            con = Constructor(tok, er_h, show_consumes)
            inte = Interpreter(con, er_h, out)
            inte.execute(show_nodes)

    else:
        line = 1
        while True:
            user = input(f"\nirb(main):00{line}:0> ")
            if user.strip() == "":
                break
            tok = Tokenizer(user + "\n", er_h)
            con = Constructor(tok, er_h)
            inte = Interpreter(con, er_h, 1)
            inte.execute(show_nodes)
            line += 1

if __name__ == "__main__":
    main()
