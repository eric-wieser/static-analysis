from structure import Joint, Mount, Beam, StructureGeometry, Loading

def test_simple():
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

def test_normal():
	a = Mount("A", [0,  0])
	b = Mount("B", [0,  254])
	c = Joint("C", [407,  0])
	d = Joint("D", [407,  200])
	e = Joint("E", [815,  0])

	ac = Beam(a, c)
	bc = Beam(b, c)
	bd = Beam(b, d)
	cd = Beam(c, d)
	ce = Beam(c, e)
	de = Beam(d, e)

	st = StructureGeometry(a)

	s = Loading(st, {e: [0, -1]})
	s.plot()
	print s.tensions

test_simple()