def my_func
  puts "Hello, world!"
  yield 3, 100
  puts "A second hello!"
  yield 5, 300
  puts "A final hello!"
end
my_func {|i, b| puts("Yielded with #{i} and #{b}")}
