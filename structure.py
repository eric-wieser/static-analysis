import numpy as np
from collections import deque

class Joint(object):
	def __init__(self, name, pos):
		self.name = name
		self.pos = np.asarray(pos)
		self.beams = set()

	def __repr__(self):
		return "{s.__class__.__name__}({s.name!r}, {s.pos!r})".format(s=self)

	def draw_to(self, axis):
		axis.text(*self.pos, s=self.name)

class Mount(Joint):
	pass

class Beam(object):
	def __init__(self, a, b):
		self.a = a
		self.b = b

		self.a.beams.add(self)
		self.b.beams.add(self)

	def __repr__(self):
		return "<Beam {s.a.name}-{s.b.name}>".format(s=self)
		# return "Beam({s.a}, {s.b})".format(s=self)

	def draw_to(self, axis, color='r', text=None):
		axis.plot(
			*zip(self.a.pos, self.b.pos),
			color=color
		)
		if text is not None:
			axis.text(*(self.a.pos + self.b.pos) / 2, s=text)

class StructureGeometry(object):
	def _walk(self, component):
		"""Find all connected components"""

		if isinstance(component, Beam):
			if component not in self.beams:
				self.beams.add(component)
				self._walk(component.a)
				self._walk(component.b)

		elif isinstance(component, Joint):
			if component not in self.joints:
				if self.dimensions is None:
					self.dimensions = len(component.pos)
				elif self.dimensions != len(component.pos):
					raise ValueError("Dimensions are not consistent!")

				self.joints.add(component)
				for beam in component.beams:
					self._walk(beam)

		else:
			raise ValueError("Unexpected component {!r}".format(component))

	def __init__(self, component):
		self.beams = set()
		self.joints = set()

		self.dimensions = None

		self._walk(component)


	def plot(self):
		import matplotlib.pyplot as plt
		from mpl_toolkits.mplot3d import Axes3D


		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)

		for b in self.beams:
			b.draw_to(ax)

		plt.show()

class NotStaticallyDeterminate(Exception):
	pass

class Loading(object):
	def __init__(self, st, forces):
		self.structure = st
		self.tensions = {}

		fail_count = 0
		to_solve = deque(st.joints)
		while to_solve:
			n = to_solve.pop()
			if self._solve(n, forces.get(n, np.zeros(st.dimensions))):
				fail_count = 0
			else:
				fail_count += 1
				to_solve.appendleft(n)

			if fail_count > len(to_solve):
				raise NotStaticallyDeterminate()

	def _solve(self, join, f):
		# nothing to resolve at mounts
		if isinstance(join, Mount):
			return True

		f = np.asarray(f)

		# find normal vectors for beams
		beam_dirs = {}
		for beam in join.beams:
			if join == beam.a:
				d = join.pos - beam.b.pos
			else:
				d = join.pos - beam.a.pos

			beam_dirs[beam] = d / np.linalg.norm(d)

		# Find unconstrained beams
		unsolved_beams = []
		for beam in join.beams:
			if beam in self.tensions:
				f -= beam_dirs[beam] * self.tensions[beam]
			else:
				unsolved_beams.append(beam)

		# not enough info to solve
		if len(unsolved_beams) > self.structure.dimensions:
			return False


		# build a matrix with the columns as unsolved beam directions
		unsolved_dir_matrix = np.array([
			beam_dirs[b] for b in unsolved_beams
		]).T

		# solve
		forces = np.linalg.solve(unsolved_dir_matrix, f)

		for beam, force in zip(unsolved_beams, forces):
			self.tensions[beam] = force

		return True

	def plot(self):
		import matplotlib.pyplot as plt
		from mpl_toolkits.mplot3d import Axes3D

		import matplotlib as mpl
		import matplotlib.cm as cm

		limit = max(abs(t) for t in self.tensions.values())
		color_mapping = cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=-limit, vmax=limit), cmap=mpl.cm.RdYlGn)


		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		ax.axis('equal')
		ax.grid()

		for b in self.structure.beams:
			t = self.tensions[b]
			b.draw_to(ax, text='{:.2f}'.format(t), color=color_mapping.to_rgba(t))

		for j in self.structure.joints:
			j.draw_to(ax)

		plt.show()