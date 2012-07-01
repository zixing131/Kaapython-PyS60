data = 1, 5, 'hello', (None,)
Tuple = ''

Tuple = reduce(lambda x, y: x + ', ' + repr(y), data, Tuple)

print Tuple, `Tuple`
Tuple = eval(Tuple)
print Tuple, `Tuple`
