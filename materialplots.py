import matplotlib.pyplot as plt
import numpy as np

from Polygon import Polygon
from Polygon.Shapes import Rectangle

import sections

def plot_modes():
	fig = plt.figure(figsize=np.array([8, 8])/2.54)
	fig.figurePatch.set_alpha(0)
	ax1 = fig.add_subplot(1, 1, 1, axisbg='white')
	ax1.tick_params(axis='both', labelsize=8)

	for mname, mode in sections.modes.iteritems():
		l_over_bs, stresses = zip(*mode)

		if mname == 'A':
			c = [0.8, 0.8, 0.8]
		elif mname == 'B':
			c = [0.6, 0.6, 0.6]
		elif mname == 'C':
			c = [0.4, 0.4, 0.4]

		ax1.plot(l_over_bs, stresses, color=np.clip(c, 0, 1))

		x, y = l_over_bs[3], stresses[3]

		ax1.annotate(
			mname,
			xy=(x,y),
			xytext=(2, 0),
			textcoords='offset points',
			color=np.clip(c, 0, 1),
			va='bottom',
			ha='left',
			fontsize=8
		)

	ax1.grid()

	ax1.set_xlabel('$L / b$')
	ax1.set_ylabel('stress / $\mathrm{N}\mathrm{mm}^{-2}$')

	fig.tight_layout()

	fig.savefig('sections-raw.png',dpi=300)
	fig.show()

def plot():
	fig = plt.figure(figsize=np.array([16, 8])/2.54,dpi=100)
	fig.figurePatch.set_alpha(0)
	ax1 = fig.add_subplot(1, 1, 1, axisbg='white')
	ax1.tick_params(axis='both', labelsize=8)

	for name, g in sections.beam_graphs.iteritems():
		if 'C' in name:
			continue

		ax1.plot(g['lengths'], g['forces'], color=g['color'])

		x, y = g['lengths'][-1], g['forces'][-1]


		ax1.annotate(
			name,
			xy=(x,y),
			xytext=(
				2 if name[1] == 'B' else -2,
				0 if int(name[0])%2 == 1 else 10
			),
			textcoords='offset points',
			color=g['color'],
			va='bottom',
			ha='left' if name[1] == 'B' else 'right',
			fontsize=8
		)

	ax1.grid()

	ax1.axis([0, 39 * 22, 0, 5000])
	ax1.set_xlabel('Length / $\mathrm{mm}$')
	ax1.set_ylabel('Compression / $\mathrm{N}$')

	fig.tight_layout()

	fig.savefig('sections.png', dpi=300)

	fig.show()

def to_poly(graph):
	return Polygon(zip(graph['lengths'], graph['forces']) + [(0, 0)])


def to_coords(poly):
	return zip(*poly[0])


def plot_areas(alpha=0.25):
	fig = plt.figure(figsize=np.array([16, 8])/2.54,dpi=100)
	fig.figurePatch.set_alpha(0)
	ax1 = fig.add_subplot(1, 1, 1, axisbg='white')
	ax1.tick_params(axis='both', labelsize=8)

	order = '1A, 2A, 3A, 1B, 4A, 5A, 2B, 3B, 4B, 6A, 5B, 6B'.split(', ')
	skip = Polygon()
	bounds = Rectangle(39 * 22, 5000)
	for n in order:
		b = sections.beam_graphs[n]
		p = to_poly(b)
		diff = bounds & (p - skip)

		skip += p

		if diff:
			for c in diff:
				ax1.fill(
					*zip(*c),
					color=b['color'], alpha=alpha)

			ax1.annotate(
				n,
				xy=diff.center(),
				textcoords='offset points',
				xytext=(0, 0) if n[1] == 'B' else (-10, -10),
				color=b['color'] * 0.5,
				va='bottom',
				ha='center',
				fontsize=8
			)
			skip += p


	ax1.grid()

	ax1.axis([0, 39 * 22, 0, 5000])
	ax1.set_xlabel('Length / $\mathrm{mm}$')
	ax1.set_ylabel('Compression / $\mathrm{N}$')

	fig.tight_layout()

	fig.savefig('areas.png', dpi=300)

	fig.show()

	return ax1

if __name__ == '__main__':
	D = 3.2
	yield_stress = 255
	for name, beam in sorted(sections.beams.iteritems()):

		effective_area = beam.area - D*beam.t - 0.5 * beam.b * beam.t
		t_max = effective_area * yield_stress

		print name, t_max

	plot_modes()
	plot()
	plot_areas()

	plt.show()