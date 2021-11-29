def fmap(x, a, b, c, d)
  return (x - a) / (b - a) * (d - c) + c
end

def printf(str)
  print str
  $stdout.flush
end

def main
  width = 25
  height = 25
  max_iter = 150
  low = -2.0
  high = 2.0

  for x in 1..(width-1) do
    for y in 1..(height-1) do
      b = fmap x, 0.0, width, low, high
      a = fmap y, 0.0, height, low, high
      ca = a
      cb = b

      z = 0
      for n in 0..(max_iter-1) do
        aa = a * a - b * b
        bb = 2 * a * b
        a = aa + ca; b = bb + cb;

        if a + b > 16
          break
        end
        z = n
      end

      brightness = fmap z, 0.0, max_iter, 0.0, 255.0
      if z == max_iter - 1
        brightness = 0
      end

      if brightness > 24
        printf "@@"
      elsif brightness > 20
        printf "%@"
      elsif brightness > 18
        printf "%%"
      elsif brightness > 16
        printf "#%"
      elsif brightness > 14
        printf "##"
      elsif brightness > 12
        printf "*#"
      elsif brightness > 10
        printf "**"
      elsif brightness > 9
        printf "+*"
      elsif brightness > 8
        printf "++"
      elsif brightness > 7
        printf "=+"
      elsif brightness > 6
        printf "=="
      elsif brightness > 5
        printf "-="
      elsif brightness > 4
        printf "--"
      elsif brightness > 3
        printf ".-"
      elsif brightness > 2
        printf ".."
      elsif brightness > 1
        printf ". "
      else
        printf "  "
      end

    end
    puts ""
  end
end

main
