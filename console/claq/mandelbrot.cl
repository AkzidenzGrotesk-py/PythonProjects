WIDTH = 100;
HEIGHT = 100;
MAX_ITER = 150;
low = -2.0;
high = 2.0;

x = 1;
y = 1;

while: x < WIDTH {
  while: y < HEIGHT {
    b = (x - 0.0) / (WIDTH - 0.0) * (high - low) + low;
    a = (y - 0.0) / (HEIGHT - 0.0) * (high - low) + low;
    ca = a;
    cb = b;

    z = 0;
    n = 0;
    while: n < MAX_ITER {
      aa = a * a - b * b;
      bb = 2 * a * b;
      a = aa + ca; b = bb + cb;

      if: a + b > 16 {
        (*) -> break;
      };
      z = n;
      n = n + 1;
    };

    brightness = (z - 0.0) / (MAX_ITER - 0.0) * (255.0 - 0.0) + 0.0;
    if: z == (MAX_ITER - 1) {
      brightness = 0;
    };

    if: brightness > 24 {
      (*"@@", true) -> print;
    } else {
    if: brightness > 20 {
      (*"%@", true) -> print;
    } else {
    if: brightness > 18 {
      (*"%%", true) -> print;
    } else {
    if: brightness > 16 {
      (*"#%", true) -> print;
    } else {
    if: brightness > 14 {
      (*"##", true) -> print;
    } else {
    if: brightness > 12 {
      (*"*#", true) -> print;
    } else {
    if: brightness > 10 {
      (*"**", true) -> print;
    } else {
    if: brightness > 9 {
      (*"+*", true) -> print;
    } else {
    if: brightness > 8 {
      (*"++", true) -> print;
    } else {
    if: brightness > 7 {
      (*"=+", true) -> print;
    } else {
    if: brightness > 6 {
      (*"==", true) -> print;
    } else {
    if: brightness > 5 {
      (*"-=", true) -> print;
    } else {
    if: brightness > 4 {
      (*"--", true) -> print;
    } else {
    if: brightness > 3 {
      (*".-", true) -> print;
    } else {
    if: brightness >2 {
      (*"..", true) -> print;
    } else {
    if: brightness > 1 {
      (*". ", true) -> print;
    } else {

      (*"  ", true) -> print;
    };
    };
    };
    };
    };
    };
    };
    };
    };
    };
    };
    };
    };
    };
    };
    };

    y = y + 1;
  };
  (*"") -> print;
  x = x + 1;
  y = 1;
};
