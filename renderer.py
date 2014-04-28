from contextlib import contextmanager

import numpy as np
import math

import structure

class Renderer(object):
	def __init__(self, obj, **kwargs):
		if isinstance(obj, structure.Loading):
			self._draw_loading(obj, **kwargs)
		elif isinstance(obj, structure.Truss):
			self._draw_structure(obj, **kwargs)

try:
	import matplotlib
	import matplotlib.pyplot
	from mpl_toolkits.mplot3d import Axes3D
except ImportError:
	pass
else:
	class MPLRenderer(Renderer):
		"""Renders using matplotlib"""

		@staticmethod
		def axisEqual3D(ax):
			ax.set_aspect("equal")
			extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
			sz = extents[:,1] - extents[:,0]
			centers = np.mean(extents, axis=1)
			maxsize = max(abs(sz))
			r = maxsize/2
			for ctr, dim in zip(centers, 'xyz'):
				getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)

		@contextmanager
		def _make_plot(self, st, w=16, h=8, setup=lambda ax: None):
			fig = matplotlib.pyplot.figure(figsize=np.array([w, h])/2.54, dpi=100)
			fig.figurePatch.set_alpha(0)
			if st.dimensions == 3:
				ax = fig.add_subplot(1, 1, 1, projection='3d')
			else:
				ax = fig.add_subplot(1, 1, 1)
				ax.margins(0.1, 0.1)
			setup(ax)
			ax.grid()

			self.dimensions = st.dimensions
			self.axis = ax
			yield

			if st.dimensions == 3:
				self.axisEqual3D(ax)
			else:
				ax.set_aspect('equal')
			matplotlib.pyplot.show()

		def _draw_structure(self, st, **kwargs):
			with self._make_plot(st, **kwargs):
				for b in st.beams:
					self._draw_beam(b)

				for j in st.joints:
					self._draw_joint(j)


		def _draw_loading(self, l, **kwargs):
			limit = max(abs(t) for t in l.tensions.values())
			color_mapping = matplotlib.cm.ScalarMappable(
				norm=matplotlib.colors.Normalize(vmin=-limit, vmax=limit),
				cmap=matplotlib.cm.RdYlGn
			)

			st = l.structure
			with self._make_plot(st, **kwargs):
				for b in st.beams:
					t = l.tensions[b]
					self._draw_beam(b, text='{:.0f}'.format(t), color=color_mapping.to_rgba(t))

				for j in st.joints:
					self._draw_joint(j)

		def _draw_beam(self, beam, color='r', text=None):
			self.axis.plot(
				*zip(beam.a.pos, beam.b.pos),
				color=color
			)
			if text is not None:
				if self.dimensions == 2:
					self.axis.annotate(
						text,
						xy=(beam.a.pos + beam.b.pos) / 2,
						textcoords='offset points',
						xytext=[-2*beam.direction[1], 2*beam.direction[0]],
						rotation=math.degrees(math.atan2(beam.direction[1], beam.direction[0])),
						color='black',
						va='bottom',
						ha='center',
						fontsize=11
					)
				else:
					self.axis.text(*(beam.a.pos + beam.b.pos) / 2, s=text)

		def _draw_joint(self, joint):
			if self.dimensions == 2:
				self.axis.annotate(
					joint.name,
					xy=joint.pos,
					color='black',
					va='center',
					ha='center',
					fontsize=11
				)
			else:
				self.axis.text(*joint.pos, s=joint.name)