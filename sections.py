from collections import namedtuple
import numpy as np
BeamCrossSection = namedtuple('BeamCrossSection', 'b t area cost color')

beams = {
	"1": BeamCrossSection(b=9.5,  t=1.6, area=27.7, cost=76,  color=np.r_[1, 0, 0]),
	"2": BeamCrossSection(b=12.5, t=1.6, area=37.6, cost=102, color=np.r_[1, 1, 0]),
	"3": BeamCrossSection(b=15.9, t=1.6, area=46.9, cost=127, color=np.r_[0, 1, 0]),
	"4": BeamCrossSection(b=16,   t=2,   area=58.7, cost=159, color=np.r_[0, 1, 1]),
	"5": BeamCrossSection(b=19.5, t=2,   area=73.2, cost=199, color=np.r_[0, 0, 1]),
	"6": BeamCrossSection(b=22,   t=3,   area=123,  cost=333, color=np.r_[1, 0, 1])
}

modes = {
	"A": [
		(0.0, 255),
		(3.0, 255),
		(12.3, 182),
		(13.2, 158),
		(14.3, 136),
		(16.1, 106),
		(18.1, 83),
		(21.2, 59),
		(23.6, 48),
		(25.8, 40),
		(28.1, 34),
		(30.3, 29),
		(33.2, 25),
		(39.0, 18)
	],

	"B": [
		(0.0, 255),
		(4.7, 255),
		(18.4, 182),
		(19.6, 162),
		(20.8, 145),
		(22.5, 121),
		(23.8, 109),
		(25.1, 96),
		(27.0, 83),
		(29.5, 70),
		(31.8, 61),
		(34.3, 53),
		(37.0, 45),
		(39.0, 40)
	],

	"C": [
		(0.0, 255),
		(6.1, 255),
		(25.0, 182),
		(26.2, 163),
		(28.5, 135),
		(31.4, 110),
		(34.5, 91),
		(37.0, 80),
		(39.0, 72)
	]
}

def is_below(xs, ys, x, y):
	for xa, xb, ya, yb in zip(xs[:-1], xs[1:], ys[:-1], ys[1:]):
		if xa < x < xb:
			y_pred = ya + (yb - ya) * (x - xa) / (xb - xa)

			return y < y_pred

	return False

def valid_sections(length, force):
	for mname, mode in modes.iteritems():
		for bname, beam in beams.iteritems():
			l_over_bs, stresses = zip(*mode)

			forces = np.array(stresses) * beam.area
			lengths = np.array(l_over_bs) * beam.b

			cost = beam.cost

			if mname in ('B', 'C'):
				forces *= 2
				cost *= 2

			if is_below(lengths, forces, length, force):
				yield bname + mname, cost

def best_section(length, force):
	return min(valid_sections(length, force), key=lambda x: x[1])

def plot():
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax1 = fig.add_subplot(1, 1, 1)

	for mname, mode in modes.iteritems():
		for bname, beam in beams.iteritems():
			l_over_bs, stresses = zip(*mode)

			forces = np.array(stresses) * beam.area
			lengths = np.array(l_over_bs) * beam.b

			if mname == 'A':
				c = beam.color * 0.5 - 0.2
			elif mname == 'B':
				c = beam.color * 0.5
				forces *= 2
			elif mname == 'C':
				c = beam.color * 0.5 + 0.2
				forces *= 2
			ax1.plot(lengths, forces, color=np.clip(c, 0, 1))

	ax1.grid()
	ax1.set_xlabel('Length / mm')
	ax1.set_ylabel('Force / N')

	plt.show()