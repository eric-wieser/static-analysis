import matplotlib.pyplot as plt
import numpy as np

import sections
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

if __name__ == '__main__':
	D = 3.2
	yield_stress = 255
	for name, beam in sorted(sections.beams.iteritems()):

		effective_area = beam.area - D*beam.t - 0.5 * beam.b * beam.t
		t_max = effective_area * yield_stress

		print name, t_max

	plot()

	plt.show()