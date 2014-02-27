from structure import Joint, Mount, Beam, StructureGeometry, Loading

a = Mount("A", [0,  0])
b = Mount("B", [0,  10])
c = Joint("C", [10,  0])
d = Joint("D", [20,  10])
e = Joint("E", [30,  0])

ac = Beam(a, c)
bc = Beam(b, c)
bd = Beam(b, d)
cd = Beam(c, d)
ce = Beam(c, e)
de = Beam(d, e)

st = StructureGeometry(a)

s = Loading(st, {e: [0, -10]})
s.plot()
print s.tensions