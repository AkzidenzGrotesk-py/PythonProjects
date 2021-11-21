# Claqulator
Programming language made in one day. Based on [calc.py](https://github.com/AkzidenzGrotesk-py/PythonProjects/blob/main/console/notruby/calc.py) in the notruby folder.

Generates tokens, builds an abstract syntax tree and executes. Has functions, but they don't get parameters.

## Hello, world!
```cl
main() {
  (*"Hello, world!") -> print;
};

(*) -> main;
```

## Name and length
```cl
nandlength() {
  (*"" + name + " (" + (*(*name) -> length) -> string + ")") -> return;
};

main() {
  name = (*"What is your name? ") -> get;
  (*"Your name is " + (*) -> nandlength) -> print;
};

(*) -> main;
```
