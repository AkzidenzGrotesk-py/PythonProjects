import sys
CMDS = {
    "00000000" : "NULL", #   null
    "00000001" : "TTMP", # * move next set to temp memory
    "00000010" : "TSTG", # * move temp memory to next set index of storage
    "00000011" : "TADD", # * add next set to temp memory
    "00000100" : "TMIN", # * minus next set to temp memory
    "00000101" : "OAND", # * and operation - from mem
    "00000110" : "OOOR", # * or operation - from mem
    "00000111" : "ONOT", #   not operation - from mem
    "00001000" : "OXOR", # * xor operation - from mem
    "00001001" : "TPTI", #   output temp memory to cmd, integer
    "00001010" : "OBSL", # * bitwise shift left - from mem
    "00001011" : "OBSR", # * bitwise shift right - from mem
    "00001100" : "STGT", # * move storage at next set index to temp memory
    "00001101" : "TPTS", #   output temp memory to cmd, char
    "00001110" : "PPTS", # * print to cmd, char (next set)
    "00001111" : "PPTI", # * print to cmd, integer (next set)
    "00010000" : "SADD", # * add next set index memory to temp memory
    "00010001" : "SMIN", # * minus next set index memory to temp memory
    "00010010" : "INPT", # * set input to temp mem
}
NXTMEM = [
    "00000001",
    "00000010",
    "00000011",
    "00000100",
    "00000101",
    "00000110",
    "00001000",
    "00001010",
    "00001011",
    "00001100",
    "00001110",
    "00001111",
    "00010000",
    "00010001",
]

def int_to_8(value):
    bnr = bin(value).replace('0b','')
    x = bnr[::-1]
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr

class KBin:
    def __init__(self, filename):
        with open(filename, "r") as bfile:
            self.text = bfile.readlines()

        for j, t in enumerate(self.text):
            self.text[j] = t.strip()
        self.text = "".join(self.text)

        if filename.split(".")[1] == "rbn":
            self.read_raw_to_cmds()
        else:
            self.read_to_commands()

        self.exec_cmds()

    def error(self, msg):
        print("\033[31merror @ " + str(self.cindex + 1) + ":\033[0m " + msg)
        sys.exit()

    def read_to_commands(self):
        self.cmds = []
        self.nxtliteral = False

        for c in range(1, int(len(self.text) / 8)+1):
            cmd = self.text[(c-1)*8:c*8]

            if self.nxtliteral:
                self.cmds.append(int(cmd, 2))
                self.nxtliteral = False
            else:
                self.cmds.append(CMDS[cmd])

                if cmd in NXTMEM:
                    self.nxtliteral = True

            print("\033[35m" + str(c) + ":\033[0m\t" + self.text[(c-1)*8:c*8] + " (" + str(int(self.text[(c-1)*8:c*8], 2)) + ") -> \t" + str(self.cmds[-1]))

    def read_raw_to_cmds(self):
        self.cmds = []
        self.nxtliteral = False
        for i, c in enumerate(self.text):
            cmd = int_to_8(ord(c))
            if self.nxtliteral:
                self.cmds.append(int(cmd, 2))
                self.nxtliteral = False
            else:
                self.cmds.append(CMDS[cmd])

                if cmd in NXTMEM:
                    self.nxtliteral = True

            print("\033[35m" + str(i+1) + ":\033[0m\t" + cmd + " (" + str(int(cmd, 2)) + ") -> \t" + str(self.cmds[-1]))


    def exec_cmds(self):
        self.tempmem = 0
        self.mem = [0 for x in range(256)]

        self.cindex = 0
        while self.cindex < len(self.cmds):
            if self.cmds[self.cindex] == "NULL":
                break
            if self.cmds[self.cindex] == "TTMP":
                self.cindex += 1
                self.tempmem = self.cmds[self.cindex]
            if self.cmds[self.cindex] == "TSTG":
                self.cindex += 1
                self.mem[self.cmds[self.cindex]] = self.tempmem
            if self.cmds[self.cindex] == "TADD":
                self.cindex += 1
                self.tempmem += self.cmds[self.cindex]
            if self.cmds[self.cindex] == "TMIN":
                self.cindex += 1
                self.tempmem -= self.cmds[self.cindex]
            if self.cmds[self.cindex] == "OAND":
                self.cindex += 1
                self.tempmem &= self.mem[self.cmds[self.cindex]]
            if self.cmds[self.cindex] == "OOOR":
                self.cindex += 1
                self.tempmem |= self.mem[self.cmds[self.cindex]]
            if self.cmds[self.cindex] == "ONOT":
                self.tempmem = ~self.tempmem
            if self.cmds[self.cindex] == "OXOR":
                self.cindex += 1
                self.tempmem ^= self.mem[self.cmds[self.cindex]]
            if self.cmds[self.cindex] == "TPTI":
                print("\033[33m" + str(self.tempmem) + "\033[0m", end = '')
            if self.cmds[self.cindex] == "OBSL":
                self.cindex += 1
                self.tempmem <<= self.mem[self.cmds[self.cindex]]
            if self.cmds[self.cindex] == "OBSR":
                self.cindex += 1
                self.tempmem >>= self.mem[self.cmds[self.cindex]]
            if self.cmds[self.cindex] == "STGT":
                self.cindex += 1
                self.tempmem = self.mem[self.cmds[self.cindex]]
            if self.cmds[self.cindex] == "TPTS":
                print("\033[33m" + str(chr(self.tempmem)) + "\033[0m", end = '')
            if self.cmds[self.cindex] == "PPTS":
                self.cindex += 1
                print("\033[33m" + str(chr(self.cmds[self.cindex])) + "\033[0m", end = '')
            if self.cmds[self.cindex] == "PPTI":
                self.cindex += 1
                print("\033[33m" + str(self.cmds[self.cindex]) + "\033[0m", end = '')
            if self.cmds[self.cindex] == "SADD":
                self.cindex += 1
                self.tempmem += self.mem[self.cmds[self.cindex]]
            if self.cmds[self.cindex] == "SMIN":
                self.cindex += 1
                self.tempmem -= self.mem[self.cmds[self.cindex]]
            if self.cmds[self.cindex] == "INPT":
                i = input()
                if i.isnumeric():
                    if int(i) < 0 or int(i) > 256:
                        self.error("input too low or too high (0-255).")
                        break
                    else: self.tempmem = int(i)
                else:
                    self.error("input must be a natural number between (0-255).")
                    break

            while self.tempmem > 255: self.tempmem -= 256


            self.cindex += 1



if __name__ == "__main__":
    if len(sys.argv) > 1:
        kb = KBin(sys.argv[1])
