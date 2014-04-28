import matplotlib.pyplot as pyplot
import numpy as np

from Polygon import Polygon
from Polygon.Shapes import Rectangle

import sections

def make_plot(w, h):
	fig = pyplot.figure(figsize=np.array([w, h])/2.54, dpi=100)
	fig.figurePatch.set_alpha(0)
	plot = fig.add_subplot(1, 1, 1, axisbg='white')
	plot.tick_params(axis='both', labelsize=8)

	return plot

def plot_modes():
	plt = make_plot(8, 8)

	for mname, mode in sections.modes.iteritems():
		l_over_bs, stresses = zip(*mode)

		if mname == 'A':
			c = [0.8, 0.8, 0.8]
		elif mname == 'B':
			c = [0.6, 0.6, 0.6]
		elif mname == 'C':
			c = [0.4, 0.4, 0.4]

		plt.plot(l_over_bs, stresses, color=np.clip(c, 0, 1))

		x, y = l_over_bs[3], stresses[3]

		plt.annotate(
			mname,
			xy=(x,y),
			xytext=(2, 0),
			textcoords='offset points',
			color=np.clip(c, 0, 1),
			va='bottom',
			ha='left',
			fontsize=8
		)

	plt.grid()
	plt.set_xlabel('$L / b$')
	plt.set_ylabel('Stress / $\mathrm{N}\mathrm{mm}^{-2}$')

	plt.figure.tight_layout(pad=0)

	plt.figure.savefig('sections-raw.png',dpi=300)
	plt.figure.show()

def plot_lines():
	plt = make_plot(16, 8)

	for name, g in sections.beam_graphs.iteritems():
		if 'C' in name:
			continue

		plt.plot(g['lengths'], g['forces'], color=g['color'])

		x, y = g['lengths'][-1], g['forces'][-1]


		plt.annotate(
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

	plt.grid()

	plt.axis([0, 39 * 22, 0, 5000])
	plt.set_xlabel('Length / $\mathrm{mm}$')
	plt.set_ylabel('Compression / $\mathrm{kN}$')

	plt.figure.tight_layout(pad=0)
	plt.figure.savefig('sections.png', dpi=300)
	plt.figure.show()


def plot_1_line():
	plt = make_plot(8, 8)

	for name, g in sections.beam_graphs.iteritems():
		if '1' not in name:
			continue

		plt.plot(g['lengths'], g['forces'], color=g['color'])

		x, y = g['lengths'][3], g['forces'][3]


		plt.annotate(
			name,
			xy=(x,y),
			xytext=(2, 0),
			textcoords='offset points',
			color=g['color'],
			va='bottom',
			ha='left',
			fontsize=8
		)

	plt.grid()

	plt.set_xlabel('Length / $\mathrm{mm}$')
	plt.set_ylabel('Compression / $\mathrm{N}$')

	plt.figure.tight_layout(pad=0)
	plt.figure.savefig('sections-1.png', dpi=300)
	plt.figure.show()

def to_poly(graph):
	return Polygon(zip(graph['lengths'], graph['forces']) + [(0, 0)])


def to_coords(poly):
	return zip(*poly[0])


def plot_areas(alpha=0.25):
	plt = make_plot(16, 8)

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
				plt.fill(
					*zip(*c),
					color=b['color'], alpha=alpha)

			plt.annotate(
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


	plt.grid()

	plt.axis([0, 39 * 22, 0, 5000])
	plt.set_xlabel('Length / $\mathrm{mm}$')
	plt.set_ylabel('Compression / $\mathrm{N}$')

	plt.figure.tight_layout(pad=0)
	plt.figure.savefig('areas.png', dpi=300)
	plt.figure.show()

	return plt

def plot_stupid_areas(alpha=0.25):
	plt = make_plot(16, 8)
	bounds = Rectangle(39 * 22, 3000)
	plt.grid()

	plt.axis([0, 39 * 22, 0, 3000])
	plt.set_xlabel('Length / $\mathrm{mm}$')
	plt.set_ylabel('Tension / $\mathrm{N}$')

	plt.fill(
		*zip(*bounds[0]),
		color=sections.beam_graphs['1A']['color'], alpha=alpha)
	plt.annotate(
		'1A',
		xy=bounds.center(),
		textcoords='offset points',
		xytext=(0, 0),
		color=sections.beam_graphs['1A']['color'] * 0.5,
		va='bottom',
		ha='center',
		fontsize=8
	)

	plt.figure.tight_layout(pad=0)
	plt.figure.show()

	return plt


if __name__ == '__main__':
	plot_modes()
	plot_1_line()
	plot_lines()
	plot_areas()

	pyplot.show()
