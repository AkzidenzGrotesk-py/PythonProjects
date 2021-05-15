# Use:
# matter(mass, density, volume) - leave one set to "False" and the rest to a number, will return the answer.
matter = lambda m, d, v: (d * v) if not m else (m / v) if not d else (m / d)

# Use
# getcontents(url) - url set to url, will return the contents of the webpage
import urllib3;from bs4 import BeautifulSoup;getcontents = lambda url:BeautifulSoup(urllib3.PoolManager().request('GET', url).data, 'html.parser')

# Generate (pseudo) random numbers using Lehmer and Wyhash (very bad, see lemire.py)
wyhash32 = lambda seed: (((((seed * 0x4a39b70d) >> 32) ^ (seed * 0x4a39b70d)) * 0x12fad5c9) >> 32) ^ ((((seed * 0x4a39b70d) >> 32) ^ (seed * 0x4a39b70d)) * 0x12fad5c9)
lehmer32 = lambda seed: (seed * 0xe120fc15) >> 32

# star
from re import sub, compile
star = lambda c: sub(compile('[\'\,\]\[]|_'), '', str([["*" for i in range(j)] for j in range(1,c+1)]).replace("], ","\n"))
# print(star(6))

# star v2
star = lambda c: print("\n".join(["".join(["*" for i in range(j)]) for j in range(1,c+1)]))
# star(5)

# Roll dice
import random
rd = lambda dice, count, pad: print((("d" + str(dice) + (" " * ((pad - 1) - len(str(dice))))) * count) + "\n" + "".join([(i + (" " * (pad - len(i)))) for i in [str(random.randrange(1, dice + 1)) for y in range(count)]]))
# rd(dice type, number of dice, padding)
# rd(6, 3, 3)
# . d6 d6 d6
# . 3  4  5
