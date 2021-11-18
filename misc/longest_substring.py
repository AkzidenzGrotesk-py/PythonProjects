def longest_substring(string: str) -> str:
  # 0 = even, 1 = odd
  simple = [int(c) % 2 for c in string]
  
  # find valid lists of alternating numbers
  valids = [[]]
  for i, s in enumerate(simple[:-1]):
    if s == simple[i + 1]: 
      if valids[-1]: 
        valids[-1].append(valids[-1][-1] + 1)
        valids.append([])
      continue
    valids[-1].append(i)

  # transpose indexes of longest and merge into string
  longest = "".join([string[i] for i in max(valids, key = len)])

  return longest


# print(longest_substring("721449827599186159274227324466"))
