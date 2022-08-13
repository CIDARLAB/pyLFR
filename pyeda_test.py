import pyeda

a, b, c, d = map(exprvar, "abcd")

f0 = ~a & b | c & ~d
f1 = a >> b

print(f0)
print(f1)

f3 = OneHot(a, b, c, d)

f1 = Or(~a & ~b & ~c, ~a & ~b & c, a & ~b & c, a & b & c, a & b & ~c)
