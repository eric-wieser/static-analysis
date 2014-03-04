from contextlib import contextmanager

import numpy as np

import structure

import matplotlib
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D


class MPLRenderer(object):
	"""Renders using matplotlib"""
	def __init__(self, obj):
		if isinstance(obj, structure.Loading):
			self._draw_loading(obj)
		elif isinstance(obj, structure.StructureGeometry):
			self._draw_structure(obj)

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
	def _make_plot(self, st):
		fig = matplotlib.pyplot.figure()
		if st.dimensions == 3:
			ax = fig.add_subplot(1, 1, 1, projection='3d')
		else:
			ax = fig.add_subplot(1, 1, 1)
			ax.axis('equal')
		ax.grid()

		self.axis = ax
		yield

		if st.dimensions == 3:
			self.axisEqual3D(ax)
		matplotlib.pyplot.show()

	def _draw_structure(self, st):
		with self._make_plot(st):
			for b in st.beams:
				self._draw_beam(b)

			for j in st.joints:
				self._draw_joint(j)


	def _draw_loading(self, l):
		limit = max(abs(t) for t in l.tensions.values())
		color_mapping = matplotlib.cm.ScalarMappable(
			norm=matplotlib.colors.Normalize(vmin=-limit, vmax=limit),
			cmap=matplotlib.cm.RdYlGn
		)

		st = l.structure
		with self._make_plot(st):

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
			self.axis.text(*(beam.a.pos + beam.b.pos) / 2, s=text)

	def _draw_joint(self, joint):
		self.axis.text(*joint.pos, s=joint.name)
