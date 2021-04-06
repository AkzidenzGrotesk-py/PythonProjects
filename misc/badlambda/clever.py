# Uses math.sin(1 / x) twice + some sigmoid as a way to encrypt.
# Written originally in a proper structure, compressed to:
clever = lambda msg, bkey, skey, mod: ''.join([chr(round(ord(j) + mod * (math.sin(1 / ( 1 / (1 + math.exp(-bkey + math.sin(1 / ( 1 / (1 + math.exp(-skey * (i / 1000))) / 100 )))) / 100 )) * 10))) for i, j in enumerate(list(msg))]);
# Usage: clever([message], [first_key], [second_key], [1 or -1 for encrypt/decrypt])
# Keys are floats.

from colorama import init
import math
init()

sigmoid = lambda x: 1 / (1 + math.exp(-x))
chaos = lambda y: math.sin(1 / ( sigmoid(y) / 100 ))

class Clever:
    def __init__(self, encode, key, switch = True):
        self.code = list(encode);
        self.key = key.split('&')
        self.start = float(self.key[0])
        self.step = float(self.key[1])

        if switch: self.encode();
        if not switch: self.decode();

    def encode(self):
        for i, j in enumerate(self.code):
            self.code[i] = chr(round(ord(j) + (chaos(self.start + chaos(self.step * (i / 1000))) * 10)));

        self.code = ''.join(self.code);
        print(self.code);

    def decode(self):
        for i, j in enumerate(self.code):
            self.code[i] = chr(round(ord(j) - (chaos(self.start + chaos(self.step * (i / 1000))) * 10)));

        self.code = ''.join(self.code);
        print(self.code);


print("\033[31mEnter a msg to encode and a key.\nKEY FORMAT: n&n, n = float between 0-10.\033[0m");
print("\033[34min ~ \033[0m", end='');e = input();
print("\033[34mkey ~ \033[0m", end='');k = input();
c = Clever(e, k);
