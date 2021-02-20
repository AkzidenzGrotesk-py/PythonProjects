# Use:
# matter(mass, density, volume) - leave one set to "False" and the rest to a number, will return the answer.
matter = lambda m, d, v: (d * v) if not m else (m / v) if not d else (m / d)
