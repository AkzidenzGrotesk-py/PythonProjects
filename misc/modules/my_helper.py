'''Helper functions and variables
DIRS_ND:            adjecent positions
DIRS_AL:            adjecent/diagonal positions
DIRS_3x3:           adjecent/diagonal/current positions
checkxy_oob:        check if an x, y position is within bounds
generate_around:    generate values "around" (and within bounds of) an x, y position.
                    what to generate around is determined by the DIRS given.
caret_H:            quickly reset the cursor
construct_mat:      generate a matrix width by height with value
shape_mat:          generate a matrix with shape, filled with value
print_len:          print object alongside its len()
file_get:           get the contents of a file
unduplicate:        remove duplicate values out of a list
flatten:            2d matrix into 1d list'''
from itertools import chain

DIRS_ND = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIRS_AL = [(-1, -1), (0, -1), (1, -1),
           (-1, 0),           (1, 0),
           (-1, 1),  (0, 1),  (1, 1)]
DIRS_3x3 = [(-1, -1), (0, -1), (1, -1),
           (-1, 0),   (0, 0),  (1, 0),
           (-1, 1),   (0, 1),  (1, 1)]


def checkxy_oob(x: int, y: int, lx: int, ly: int) -> bool:
    '''Check if value x OR y is OOB,
    which is defined as lx - 1|ly - 1 > x|y > 0.
    If you have a matrix, just give
    len(mat[0]) and len(mat) as lx and ly.'''
    return x < 0 or y < 0 or x > lx - 1 or y > ly - 1

def generate_around(x: int, y: int, lx: int, ly: int, around: list[tuple]) -> list[tuple]:
    '''Generate all positions around x and y,
    using around list (DIRS_ND, DIRS_AL, etc.) and
    return all values that are in bounds (check_matrix_oob).
    If you have a matrix, just give
    len(mat[0]) and len(mat) as lx and ly.'''
    return [
        (x + mx, y + my)
        for mx, my in around
        if not checkxy_oob(x + mx, y + my, lx, ly)
    ]

def caret_H(x: int = 0, y: int = 0) -> None:
    '''Move text cursor in console.'''
    print(f"\033[{y};{x}H", end = "")

def construct_mat(width: int, height: int, value: int = 0) -> list[list]:
    '''Construct a matrix width by height containing value.'''
    return [[value for _ in range(width)] for _ in range(height)]

def shape_mat(mat: list[list], value: int = 0) -> list[list]:
    '''Construct a matrix with the same shape as mat'''
    return [[value for _ in line] for line in mat]

def print_len(thing) -> None:
    '''Print thing with the length'''
    print(f"({len(thing)}) {thing}")

def file_get(filename: str) -> str:
    '''Get contents of a file'''
    with open(filename, "r", encoding = "utf-8") as file:
        contents = file.read()
    return contents

def unduplicate(thing: list) -> list:
    '''Remove duplicates out of list'''
    return list(dict.fromkeys(thing))

def flatten(thing: list[list]) -> list:
    '''Turn a matrix into a list'''
    return list(chain.from_iterable(thing))
