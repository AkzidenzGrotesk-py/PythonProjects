# Use:
# matter(mass, density, volume) - leave one set to "False" and the rest to a number, will return the answer.
matter = lambda m, d, v: (d * v) if not m else (m / v) if not d else (m / d)

# Use
# getcontents(url) - url set to url, will return the contents of the webpage
import urllib3;from bs4 import BeautifulSoup;getcontents = lambda url:BeautifulSoup(urllib3.PoolManager().request('GET', url).data, 'html.parser')

# Generate (pseudo) random numbers using Lehmer and Wyhash (very bad, see lemire.py)
wyhash32 = lambda seed: (((((seed * 0x4a39b70d) >> 32) ^ (seed * 0x4a39b70d)) * 0x12fad5c9) >> 32) ^ ((((seed * 0x4a39b70d) >> 32) ^ (seed * 0x4a39b70d)) * 0x12fad5c9)
lehmer32 = lambda seed: (seed * 0xe120fc15) >> 32
