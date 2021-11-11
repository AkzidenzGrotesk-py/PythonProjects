from dataclasses import dataclass
import string, sys, math

VALID_CHARS = string.ascii_uppercase + string.ascii_lowercase + "_"

@dataclass
class Token:
  id: str
  value: str

class Eqed:
  def __init__(self, equation: str):
    self.equation = equation
    self.char = -1
    self.final = ["", "", ""]

  def error(self, msg):
    print(f"\033[31;1merror: {msg}\033[0m")
    sys.exit()


  def advance(self):
    if self.char > len(self.equation) - 1:
      return
    self.char += 1

  def backtrack(self):
    if self.char < 1: return
    self.char -= 1

  def collect_sig(self):
    col = ""
    self.advance()
    while self.equation[self.char] in VALID_CHARS:
      col += self.equation[self.char]
      self.advance()

      if self.char > len(self.equation) - 1: self.error("reached EOF")

    self.backtrack()

    return col

  def collect_sub(self):
    col = ""
    cot = 1
    self.advance()
    while cot > 0:
      col += self.equation[self.char]
      self.advance()
      if self.equation[self.char] == "{": cot += 1
      if self.equation[self.char] == "}": cot -= 1
      if self.char > len(self.equation) - 1: self.error("reached EOF")

    return col

  def next(self):
    self.advance()

    if self.char > len(self.equation) - 1:
      return Token("EOF", "end of file")

    while self.equation[self.char] in [" ", "\t", "\n", "\r"]: self.advance()

    if self.equation[self.char] == "~":
      return Token("SYM", self.collect_sig())

    elif self.equation[self.char] == "{":
      return Token("INE", self.collect_sub())

    elif self.equation[self.char] == "=":
      return Token("EQL", "=")

    elif self.equation[self.char] == "+":
      return Token("PLS", "+")

    elif self.equation[self.char] == "-":
      return Token("MIN", "-")

    elif self.equation[self.char] == "*":
      return Token("MUL", "×")

    elif self.equation[self.char] == "/":
      return Token("DIV", "÷")

    return Token("GEN", self.equation[self.char])

  def mid_index(self, l) -> int:
    return math.floor(len(l) / 2)

  def add_final_center(self, value, voffset):
    self.final[1] += value
    self.final[0] += " " * voffset
    self.final[2] += " " * voffset

  def add_final_top(self, value, voffset):
    self.final[0] += value
    self.final[1] += " " * voffset
    self.final[2] += " " * voffset

  def add_final_btm(self, value, voffset):
    self.final[2] += value
    self.final[0] += " " * voffset
    self.final[1] += " " * voffset

  def convert(self) -> str:
    self.end_found = False

    while not self.end_found:
      self.tok = self.next()

      if self.tok.id == "EOF":
        self.end_found = True

      if self.tok.id == "GEN": self.add_final_center(self.tok.value, 1)

      if self.tok.id in ["EQL", "PLS", "MIN", "MUL", "DIV"]:
        self.add_final_center(" " + self.tok.value + " ", 3)

      if self.tok.id == "SYM":
        if self.tok.value == "frac":
          self.tok = self.next()
          if self.tok.id == "INE":
            n = Eqed(self.tok.value).convert()
            self.tok = self.next()
            if self.tok.id == "INE":
              n2 = Eqed(self.tok.value).convert()
              self.final[1] += "—" * max(len(n), len(n2))
              self.final[0] += n
              self.final[2] += n2

            else: self.error("missing fraction bottom")
          else: self.error("missing fraction top")

        elif self.tok.value == "esc":
          self.tok = self.next()
          if self.tok.id == "INE":
            self.add_final_center(self.tok.value, len(self.tok.value))
          else: self.error("missing character to escape")

        elif self.tok.value == "super":
          self.tok = self.next()
          if self.tok.id == "INE":
            self.add_final_top(self.tok.value, len(self.tok.value))
          else: self.error("missing character to superscript")

        elif self.tok.value == "sub":
          self.tok = self.next()
          if self.tok.id == "INE":
            self.add_final_btm(self.tok.value, len(self.tok.value))
          else: self.error("missing character to subscript")

        elif self.tok.value == "msuper":
          self.tok = self.next()
          if self.tok.id == "INE":
            self.add_final_center(self.tok.value.replace("0", "⁰").replace("1", "¹").replace("2", "²").replace("3", "³").replace("4", "⁴").replace("5", "⁵").replace("6", "⁶").replace("7", "⁷").replace("8", "⁸").replace("9", "⁹").replace("+", "⁺").replace("-", "⁻").replace("=", "⁼").replace("(", "⁽").replace(")", "⁾"), len(self.tok.value))
          else: self.error("missing character to superscript")

        elif self.tok.value == "msub":
          self.tok = self.next()
          if self.tok.id == "INE":
            self.add_final_center(self.tok.value.replace("0", "₀").replace("1", "₁").replace("2", "₂").replace("3", "₃").replace("4", "₄").replace("5", "₅").replace("6", "₆").replace("7", "₇").replace("8", "₈").replace("9", "₉").replace("+", "₊").replace("-", "₋").replace("=", "₌").replace("(", "₍").replace(")", "₎"), len(self.tok.value))
          else: self.error("missing character to subscript")

        elif self.tok.value == "theta":
          self.add_final_center("θ", 1)

        else: self.error(f"unrecognized symbol -> {self.tok.value}")


    # print(self.final)
    if self.final[0].strip() != "":
      self.final = "\n".join(self.final)
    else:
      self.final = self.final[0].strip() + self.final[1] + self.final[2].strip()
    #t = Token("NULL", "")
    #while t.id != "EOF":
    #  t = self.next()
    #  print(t)

    return self.final


  

def main():
  e = Eqed("tan~theta=~frac{b}{a}").convert()
  print("\n" + e + "\n")

if __name__ == "__main__":
  main()
