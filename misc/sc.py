#
# This language is split into stored in a set of 'slots', with IDs a-zA-Z0-9
# We can write data to a slot using the @ symbol.
# @[slot]:[data], @a:41 -> 4 + 1 is written to slot 'a'
#
# Slots can be reformatted to hold strings instead of numerical values, this also clears the value.
# -[slot][new format code], -b# -> sets b to 0, -a" -> sets a to ""
#
# We can also use slot clearing to write
# -a":hello, world!
#
# Sometimes we need an arbitrary character which does nothing, this is the pipe '|'
# Whitespace is also unnoticed
#
# When writing to slots with numerical format, we can use the < and > operators to shift which digit we write to.
# @a:<<<3 -> 3000 is written to a
# @a:3<4<5 -> 543 is written to a
# @a:>3 -> .3 is written to a
#
# We can also search for input using the ? operator
# ?[number of characters to print][characters]
# @a:<?2> | -> asks for input '> '
# If your code ends in a important piece of whitespace, always add a | to mark the end.
#
# Alternatively, you can use a breakpoint character
# @a:?*enter a number: *| -> asks for input 'enter a number: '
#
# We can get data from other slots using the &[slot] operator
# @a:5-b":The number five! &a |
# If we do not want decimal points
# &<a
#
# We can output using a < operator with the slot
# @a:5|<a
# Don't forget the pipe to break the reading
#
# Change how a value is added to a slot using +/~/*//
# @a:5*3|<a
#
# BRANCHING
# {[comparison type][value A][value B][run if true]}
# @a:3@b:4|{=ab-v":A = B"<v}|{!ab-v":A =/= B"<v}|
#
# e.g. "password checker": -P":unicorns"-p":?'Enter password: '"{=pP-v":You got the password correct!"<v}|{!pP-v":Incorrect password!"<v}|
# Get name example
# -b":Your name is ?6name- |
import string, sys

breakers = ['@', '-', '|', '\"']

data = {
    d : 0 for d in (string.ascii_lowercase + string.ascii_uppercase + string.digits)
}

def error(text: str, cl: int) -> None:
    print(f"\033[31m[! @ {cl + 1}]  {text}\033[0m")

def read(text: str) -> bool:
    read_in = 'a'
    c = 0
    cchar = ''
    for _c, _cchar in enumerate(text):
        if _c > c: c += 1
        elif c > _c: continue
        cchar = _cchar

        if cchar == ' ': continue
        if cchar == '@':
            c += 1; cchar = text[min(len(text) - 1, c)]
            if cchar in data:
                read_in = cchar
                c += 1; cchar = text[min(len(text) - 1, c)]
                continue
            else:
                error(f"attempting to write to non-existant slot [{cchar}], use a-zA-z0-9", c)
                return False
        if cchar == '-':
            c += 1; cchar = text[min(len(text) - 1, c)]
            if cchar in data:
                read_in = cchar
                c += 1; cchar = text[min(len(text) - 1, c)]
                if cchar == "#": data[read_in] = 0.0
                elif cchar == "\"": data[read_in] = ""
                else:
                    error("cannot read replace type", c)
                    return False
                c += 1; cchar = text[min(len(text) - 1, c)]
                continue
            else:
                error(f"attempting to write to non-existant slot [{cchar}], use a-zA-z0-9", c)
                return False
        if cchar == ':':
            read_place = 1.0
            read_op = '+'
            while not text[min(len(text) - 1, c+1)] in breakers and c < (len(text) - 1):
                c += 1; cchar = text[min(len(text) - 1, c)]
                dl = data[read_in]
                if type(dl) == str:
                    if cchar in ['?', '&']:
                        if cchar == '?':
                            c += 1; cchar = text[c]
                            gs = ""
                            if cchar.isnumeric():
                                for j in range(int(cchar)):
                                    c += 1; cchar = text[min(len(text) - 1, c)]

                                    if not c < (len(text) - 1):
                                        error(f"hit EOF while trying to collect input string", c)
                                        return False

                                    gs += cchar

                            elif not cchar.isnumeric():
                                bp = cchar
                                fl = True
                                c += 1; cchar = text[min(len(text) - 1, c)]
                                while cchar != bp:
                                    if not fl: c += 1; cchar = text[min(len(text) - 1, c)]
                                    fl = False

                                    if not c < (len(text) - 1):
                                        error(f"hit EOF while trying to collect input string", c)
                                        return False

                                    if cchar != bp: gs += cchar

                            i = input(f"{gs}")
                            data[read_in] += str(i)

                        elif cchar == '&':
                            c += 1; cchar = text[min(len(text) - 1, c)]

                            if not cchar in data:
                                if cchar == '<':
                                    c += 1; cchar = text[min(len(text) - 1, c)]
                                    if type(data[cchar]) in [int, float]:
                                        data[read_in] += str(round(data[cchar]))

                            else: data[read_in] += str(data[cchar])
                            # c += 1; cchar = text[min(len(text) - 1, c)]

                        continue
                    data[read_in] += str(cchar)
                elif type(dl) == int or type(dl) == float:
                    if cchar in ['>', '<', '?', '&', '*', '+', '/', '~']:
                        if cchar == '>': read_place = round(read_place * 0.1, 8)
                        elif cchar == '<': read_place = round(read_place * 10, 8)
                        elif cchar == '&':
                            c += 1; cchar = text[min(len(text) - 1, c)]
                            if type(data[cchar]) == int or type(data[cchar]) == float:
                                if read_op == '+': data[read_in] += data[cchar] * read_place
                                elif read_op == '*': data[read_in] *= data[cchar] * read_place
                                elif read_op == '/': data[read_in] /= data[cchar] * read_place
                                elif read_op == '~': data[read_in] -= data[cchar] * read_place
                            else:
                                error(f"cannot add data in string area to data in numerical area", c)
                                return False
                            # c += 1; cchar = text[min(len(text) - 1, c)]
                        elif cchar in ['*', '+', '/', '~']:
                            read_op = cchar
                            # c += 1; cchar = text[min(len(text) - 1, c)]
                        elif cchar == '?':
                            c += 1; cchar = text[min(len(text) - 1, c)]
                            gs = ""
                            if cchar.isnumeric():
                                for j in range(int(cchar)):
                                    c += 1; cchar = text[min(len(text) - 1, c)]

                                    if not c < (len(text) - 1):
                                        error(f"hit EOF while trying to collect input string", c)
                                        return False

                                    gs += cchar

                            elif not cchar.isnumeric():
                                bp = cchar
                                fl = True
                                c += 1; cchar = text[min(len(text) - 1, c)]
                                while cchar != bp:
                                    if not fl: c += 1; cchar = text[min(len(text) - 1, c)]
                                    fl = False

                                    if not c < (len(text) - 1):
                                        error(f"hit EOF while trying to collect input string", c)
                                        return False

                                    if cchar != bp: gs += cchar

                            i = input(f"{gs}")
                            if i.isnumeric():
                                if read_op == '+': data[read_in] += float(i) * read_place
                                elif read_op == '*': data[read_in] *= float(i) * read_place
                                elif read_op == '/': data[read_in] /= float(i) * read_place
                                elif read_op == '~': data[read_in] -= float(i) * read_place
                            else:
                                error(f"input provided must be numeric", c)
                                return False
                        continue

                    if not cchar.isnumeric():
                        error(f"attemping to add non-numeric character [{cchar}]", c)
                        return False
                    if read_op == '+': data[read_in] += float(cchar) * read_place
                    elif read_op == '*': data[read_in] *= float(cchar) * read_place
                    elif read_op == '/': data[read_in] /= float(cchar) * read_place
                    elif read_op == '~': data[read_in] -= float(cchar) * read_place
            c += 1; cchar = text[min(len(text) - 1, c)]
            continue
        if cchar == '<':
            c += 1; cchar = text[min(len(text) - 1, c)]
            if cchar in data:
                print(data[cchar])
                c += 1; cchar = text[min(len(text) - 1, c)]
            else:
                error(f"cannot output from non-existant slot [{cchar}]", c)
            continue
        if cchar == '{':
            c += 1; cchar = text[min(len(text) - 1, c)]
            if cchar in ["=", "!"]:
                op_type = cchar
                c += 1; cchar = text[min(len(text) - 1, c)]
                if cchar in data: term1 = data[cchar]
                c += 1; cchar = text[min(len(text) - 1, c)]
                if cchar in data: term2 = data[cchar]

                cv = ""
                ntf = 1
                while ntf > 0:
                    c += 1; cchar = text[min(len(text) - 1, c)]

                    if not c < (len(text) - 1):
                        error(f"hit EOF while trying to collect input string", c)
                        return False

                    #if cchar != '}' and ntf == 1: cv += cchar
                    #else:
                    if cchar == '{': ntf += 1
                    if cchar == '}': ntf -= 1

                    cv += cchar
                cv = cv[:-1]

                if op_type == '=' and term1 == term2 or op_type == '!' and term1 != term2: read(cv)
                c += 1; cchar = text[min(len(text) - 1, c)]


        if cchar == '|' or cchar == '\"': continue

        error(f"unrecognized character [{cchar}]", c)
        return False


    #for d in data:
    #    if data[d] != 0: print(f"{d} -> {data[d]}")

    return True

def main() -> None:
    if len(sys.argv) == 1:
        while True:
            i: str = input("\n~$ ").replace('\n','').replace('\t','')
            if not i: break
            read(i)
    else:
        with open(sys.argv[1], "r") as file:
            read(file.read().replace('\n','').replace('\t',''))

if __name__ == '__main__':
    main()
