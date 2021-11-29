'''
ErrorHandler for Pyrite.
'''

from sys import exit as sysexit

class ErrorHandler:
    '''
    Return errors.
    '''
    def __init__(self, end_on_error = True):
        self.pos = 0
        self.eoe = end_on_error

    def reset_pos(self):
        '''Sets 'cursor' position to 0.'''
        self.pos = 0

    def token_error(self, description: str):
        '''Errors from Tokenizer'''
        print(f"\033[31m[ERROR] @ c:{self.pos} -> {description} in Tokenizer.\033[0m")
        sysexit(1)

    def construct_error(self, description: str):
        '''Errors from Constructor'''
        print(f"\033[31m[ERROR] @ t:{self.pos} -> {description} in Constructor.\033[0m")
        sysexit(1)

    def interpret_error(self, description: str):
        '''Errors from Interpreter'''
        print(f"\033[31m[ERROR] @ n:{self.pos} -> {description} in Interpreter.\033[0m")
        sysexit(1)

    def interpret_warning(self, description: str):
        '''Warning from Interpreter'''
        print(f"\033[33m[WARNING] @ n:{self.pos} -> {description} in Interpreter.\033[0m")
