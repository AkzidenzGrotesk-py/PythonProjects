from math import sqrt
from itertools import count, islice

def ftree_node(n):
    f = [j for j in range(1, n + 1) if n % j == 0]
    if len(f) < 2: return f
    o = [f[1], int(n / f[1]), ftree_node(f[-2]) if not (f[-2] > 1 and all(f[-2] % i for i in islice(count(2), int(sqrt(f[-2]) - 1)))) else f[-2]]
    if type(o[2]) != list: del o[1]
    return o

def ftree(n):
    return [n, ftree_node(n)]

def render_tree(tree, depth = 0):
    dtabs = (' ' * depth) + '└─'
    if len(tree) == 3:
        return f"{dtabs}{tree[0]}\n{dtabs}{tree[1]}\n{render_tree(tree[2], depth + 1)}"
    else:
        return f"{dtabs}{tree[0]}\n{dtabs}{tree[1]}"

      
def main():
    print(render_tree(ftree_node(int(input("> ")))))
    
if __name__ == '__main__':
    main()
