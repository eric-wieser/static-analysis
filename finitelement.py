import itertools
import math

from structure import Joint, Mount, Beam, StructureGeometry, Loading
from renderer import MPLRenderer as display

import sections

import numpy as np

def show_cost(loading):
	c_cost = 0
	for beam, tension in loading.tensions.iteritems():
		l = beam.length / 1000
		if tension < 0:
			name, cost_l = sections.best_section(beam.length, -tension)
			c_cost += l * cost_l

			print beam, ':', name
		else:
			b = sections.beams["1"]
			c_cost += l * b.linear_density * 500

	print "Cost:", c_cost

def get_cost(loading):
	c_cost = 0
	for beam, tension in loading.tensions.iteritems():
		l = beam.length / 1000
		if tension < 0:
			try:
				name, cost_l = sections.best_section(beam.length, -tension)
			except ValueError:
				return float('inf')
			c_cost += l * cost_l
		else:
			b = sections.beams["1"]
			c_cost += l * b.linear_density * 500

	return c_cost

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
	display(s)

def make_half():
	a = Mount('A', np.array([   0.,    0.]))
	b = Mount('B', np.array([   0.,  254.]))
	c = Joint('C', np.array([ 451.,    0.]))
	d = Joint('D', np.array([ 612.,  197.]))
	e = Joint('E', np.array([ 910.,    0.]))

	ac = Beam(a, c)
	bc = Beam(b, c)
	bd = Beam(b, d)
	cd = Beam(c, d)
	ce = Beam(c, e)
	de = Beam(d, e)

	return StructureGeometry(a)


def test_normal():
	st = make_half()

	l = Loading(st, {st['E']: [0, -1000]})
	show_cost(l)

	display(l)


def test_normal3D():
	new_x = 815 / math.sqrt(407**2 + 815**2)
	new_z = 407 / math.sqrt(407**2 + 815**2)

	st = make_half()

	matrix = np.array([
		[new_x,  0],
		[new_z,  0],
		[0,      1]
	])

	a_pos = np.dot(matrix, st['A'].pos)
	b_pos = np.dot(matrix, st['B'].pos)
	c_pos = np.dot(matrix, st['C'].pos)
	d_pos = np.dot(matrix, st['D'].pos)
	e_pos = np.dot(matrix, st['E'].pos)

	y_offset = np.array([0, 57.5, 0])
	z_offset = np.array([0, 0, -57.5])

	a = Mount("A", a_pos + y_offset)
	b = Mount("B", b_pos + y_offset)
	c = Joint("C", c_pos + y_offset)
	d = Joint("D", d_pos + y_offset)
	e = Joint("E", e_pos + y_offset)

	a_ = Mount("A'", a_pos - y_offset)
	b_ = Mount("B'", b_pos - y_offset)
	c_ = Joint("C'", c_pos - y_offset)
	d_ = Joint("D'", d_pos - y_offset)
	e_ = Joint("E'", e_pos - y_offset)

	f = Joint("F", e_pos + z_offset)

	Beam(c, c_)
	Beam(d, d_)
	Beam(e, e_)

	Beam(e, f)
	Beam(e_, f)

	ac = Beam(a, c)
	bc = Beam(b, c)
	bd = Beam(b, d)
	cd = Beam(c, d)
	ce = Beam(c, e)
	de = Beam(d, e)

	a_c_ = Beam(a_, c_)
	b_c_ = Beam(b_, c_)
	b_d_ = Beam(b_, d_)
	c_d_ = Beam(c_, d_)
	c_e_ = Beam(c_, e_)
	d_e_ = Beam(d_, e_)

	Beam(c, e_)
	Beam(a, c_)
	Beam(b, d_)

	st = StructureGeometry(a)

	from pprint import pprint
	pprint(st.joints)

	display(st)

	l = Loading(st, {f: [0, 0, -2000]})
	show_cost(l)

	display(l)


def test_ridiculous3D():


	a = Mount("A", [0,    80, 0])
	a_ = Mount("A'", [0,   -80, 0])
	b = Mount("B", [0,    0, 254])


	c =  Joint("C", [400,    80, 254])
	c_ = Joint("C'", [400,    -80, 254])

	d = Joint("D", [400,    0, 0])

	e = Joint("E", [800,    0, 0])

	Beam(a, c)
	Beam(a_, c_)
	Beam(b, c)
	Beam(b, c_)
	# Beam(c, c_)


	Beam(a, d)
	Beam(a_, d)
	Beam(c, d)
	Beam(c_, d)
	Beam(d, e)
	Beam(c, e)
	Beam(c_, e)


	# a_ = Mount("A'", [0,   -80, 0])
	# b_ = Mount("B'", [0,   -80, 254])
	# c_ = Joint("C'", [407, 163.5, 0])
	# d_ = Joint("D'", [407, 163.5, 200])

	# ac = Beam(a, c)
	# bc = Beam(b, c)
	# bd = Beam(b, d)
	# cd = Beam(c, d)
	# ce = Beam(c, e)
	# de = Beam(d, e)

	# a_c_ = Beam(a_, c_)
	# b_c_ = Beam(b_, c_)
	# b_d_ = Beam(b_, d_)
	# c_d_ = Beam(c_, d_)
	# c_e = Beam(c_, e)
	# d_e = Beam(d_, e)

	# d_d = Beam(d_, d)
	# c_c = Beam(c_, c)

	# ac_ = Beam(a, c_)
	# bd_ = Beam(b, d_)

	st = StructureGeometry(a)

	display(st)

	l = Loading(st, {e: [0, 0, -1000]})
	show_cost(l)

	display(l)

def optimize_normal():
	a = Mount('A', array([   0.,    0.]))
	b = Mount('B', array([   0.,  254.]))
	c = Joint('C', array([ 451.,    0.]))
	d = Joint('D', array([ 612.,  197.]))
	e = Joint('E', array([ 910.,    0.]))

	ac = Beam(a, c)
	bc = Beam(b, c)
	bd = Beam(b, d)
	cd = Beam(c, d)
	ce = Beam(c, e)
	de = Beam(d, e)

	st = StructureGeometry(a)

	load = {e: [0, -1000]}

	best_f = float('inf')
	best = []

	# list of vector offsets to try over [-400, 400]^2
	d_poses = d.pos + np.mgrid[-5:5:21j, -5:5:21j].T.reshape(-1, 2)
	c_poses = c.pos + np.r_[1, 0] * np.r_[-5:5:21j][:, np.newaxis]
	# c_poses = c.pos + np.mgrid[-400:400:20j, -400:400:20j].T.reshape(-1, 2)

	print "tests"

	for d_pos, c_pos in itertools.product(d_poses, c_poses):
		d.pos = d_pos
		c.pos = c_pos
		try:
			s = Loading(st, load)
			max_f = get_cost(s) #sum(t*t for t in s.tensions.values())

			if max_f < best_f:
				best_f = max_f
				best = [(d_pos, c_pos)]
			elif max_f == best_f:
				best_f = max_f
				best.append((d_pos, c_pos))
		except np.linalg.linalg.LinAlgError:
			pass

	print best[:10]

	d.pos = best[0][0]
	c.pos = best[0][1]
	for j in st.joints:
		print j
	s = Loading(st, load)

	show_cost(s)
	display(s)


test_normal3D()
# optimize_normal()
#test_normal()