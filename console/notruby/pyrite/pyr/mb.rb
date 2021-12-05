def fmap(x, a, b, c, d)
  return (x - a) / (b - a) * (d - c) + c
end

def main
  width = 50
  height = 50
  max_iter = 150
  low = -2.0
  high = 2.0

  for x in 1..(width-1) do
    for y in 1..(height-1) do
      b = fmap(x, 0.0, width, low, high)
      a = fmap(y, 0.0, height, low, high)
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

      brightness = fmap(z, 0.0, max_iter, 0.0, 255.0)
      if z == max_iter - 1
        brightness = 0
      end

      if brightness > 24
        print "@@"
      elsif brightness > 20
        print "%@"
      elsif brightness > 18
        print "%%"
      elsif brightness > 16
        print "#%"
      elsif brightness > 14
        print "##"
      elsif brightness > 12
        print "*#"
      elsif brightness > 10
        print "**"
      elsif brightness > 9
        print "+*"
      elsif brightness > 8
        print "++"
      elsif brightness > 7
        print "=+"
      elsif brightness > 6
        print "=="
      elsif brightness > 5
        print "-="
      elsif brightness > 4
        print "--"
      elsif brightness > 3
        print ".-"
      elsif brightness > 2
        print ".."
      elsif brightness > 1
        print ". "
      else
        print "  "
      end

    end
    puts ""
  end
end

main
