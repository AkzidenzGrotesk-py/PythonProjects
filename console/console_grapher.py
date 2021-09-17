import sys, os

SW_min = -15
SH_min = -15
SW_max = 15
SH_max = 15

def graph_string_function(x: float, fx: str) -> float:
  fx = fx.lower().replace("x", str(x))
  try: 
    e = eval(fx)
    return e
  except NameError: 
    print("Only variables \033[33mx\033[0m & \033[33my\033[0m are accessible at this time.")
    sys.exit()

def render(f: str) -> None:
  global SW_min, SH_min, SW_max, SH_max
  
  # // SETTING UP SCREEN
  screen = [[" " for x in range(-SW_max, -SW_min)] for y in range (-SH_max, -SH_min)]
  for y, c in enumerate(screen):
    for x, _ in enumerate(c):
      if -x + SW_max == 0: screen[y][x] = '|'
      elif -y + SH_max == 0: screen[y][x] = '—'

  # // GRAPHING
  x = -SW_max + 1
  while x < -SW_min:
    ypos = graph_string_function(x, f)
    ay = -ypos + SH_max
    if 0 <= ay < SH_max - SH_min: screen[round(ay)][round(x + SW_max)] = "\033[33m#\033[0m"

    x += 0.1


  # // RENDERING
  render = ""
  for y in screen:
    for x in y:
      render += x + " "
    render += '\n'
  print(render)

def main() -> None:
  global SW_min, SH_min, SW_max, SH_max

  while True:
    # // GETTING INPUT
    f = input("\n> ").lower()
    if f.strip() == "": break
    if f.split()[0] == "edge":
      nv = int(input("\tenter new size > "))
      SW_min = -nv
      SH_min = -nv
      SW_max = nv
      SH_max = nv
      continue

    # // EXECUTE
    os.system("clear")
    print(f"y = {f}\n")
    render(f)



if __name__ == '__main__':
  main()
