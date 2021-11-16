m = lambda multi, tofrom, word: [word if i % multi == 0 else "" for i in range(*tofrom)]
merge = lambda listA, listB: [listA[i] + listB[i] for i in range(min(len(listA), len(listB)))]
mod_v = lambda listA, value: [l + value for l in listA]

ranges = (1, 101)
fizz = m(3, ranges, "Fizz")
buzz = m(5, ranges, "Buzz")
fizzbuzz = merge(fizz, buzz) # or merge(m(3, ranges, "Fizz"), m(5, ranges, "Buzz"))
fizzbuzz = [fizzbuzz[i] if fizzbuzz[i] else str(i + 1) for i in range(*mod_v(ranges, -1))]
