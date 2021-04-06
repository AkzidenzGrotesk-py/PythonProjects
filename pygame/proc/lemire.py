import datetime, time

# Implementation of https://lemire.me/blog/2019/03/19/the-fastest-conventional-random-number-generator-that-can-pass-big-crush/
# Using time: microseconds.
# Will probably make a badlambda version
class dlRandom:
    def __init__(self, seed = 0):
        self.ms = datetime.datetime.now()
        if seed == 0: self.seed = int(self.ms.strftime("%f"))
        else: self.seed = seed

    def __seed__(self, nseed):
        self.seed = round(nseed)
    
    def wyhash32(self):
        self.seed += 0xe120fc15
        tmp = self.seed * 0x4a39b70d
        m1 = (tmp >> 32) ^ tmp
        tmp = m1 * 0x12fad5c9
        m2 = (tmp >> 32) ^ tmp
        return m2;

    def lehmer32(self):
        self.seed *= 0xe120fc15
        return self.seed >> 32

    def integer(self, nmin, nmax, method = 1):
        if method == 1: return self.wyhash32() % (nmax - nmin) + nmin
        if method == 2: return self.lehmer32() % (nmax - nmin) + nmin

    def double(self, nmin, nmax, method = 1):
        if method == 1: return (self.wyhash32() / 0x7FFFFFFF) * (nmax - nmin) + nmin
        if method == 2: return (self.lehmer32() / 0x7FFFFFFF) * (nmax - nmin) + nmin
    

print(dlRandom().integer(0, 100))
