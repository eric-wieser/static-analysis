import numpy as np
import scipy.stats
from collections import deque


class Joint(object):
	"""A pin joint"""
	def __init__(self, name, pos):
		self.name = name
		self.pos = np.asarray(pos)
		self.beams = set()

	def __repr__(self):
		return "{s.__class__.__name__}({s.name!r}, {s.pos!r})".format(s=self)

class Mount(Joint):
	"""A joint at which an arbitrary external reaction force is applied"""
	pass

class Beam(object):
	"""A connection between two joints"""
	def __init__(self, a, b):
		self.a = a
		self.b = b

		self.a.beams.add(self)
		self.b.beams.add(self)

	def __repr__(self):
		return "<Beam {s.a.name}-{s.b.name}>".format(s=self)

	@property
	def length(self):
		return np.linalg.norm(self.b.pos - self.a.pos)

	@property
	def direction(self):
		"""The unit vector pointing from a to b"""
		return (self.b.pos - self.a.pos) / self.length


class Truss(object):
	"""A collections of Beams and joints"""
	def __init__(self, component):
		self.beams = set()
		self.joints = set()

		self.dimensions = None

		self._walk(component)

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


	def __getitem__(self, x):
		"""Access components by name"""
		if isinstance(x, tuple):
			x = set(x)
			return next(b for b in self.beams if set([b.a.name, b.b.name]) == x)
		else:
			return next(j for j in self.joints if j.name == x)


class NotStaticallyDeterminate(Exception):
	"""Indicates that the structure cannot be analyzed solely by pin-jointed analysis"""
	pass

class Loading(object):
	"""A loading configuration of a structure"""
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

	def _solve(self, joint, f):
		"""Attempt to resolve forces at a single joint, if possible"""
		# nothing to resolve at mounts
		if isinstance(joint, Mount):
			return True

		f = np.asarray(f)

		# calculate direction vectors for beams
		beam_dirs = {}
		for beam in joint.beams:
			if joint == beam.a:
				beam_dirs[beam] = beam.direction
			else:
				beam_dirs[beam] = -beam.direction

		# find unconstrained beams
		unsolved_beams = []
		for beam in joint.beams:
			if beam in self.tensions:
				f += beam_dirs[beam] * self.tensions[beam]
			else:
				unsolved_beams.append(beam)

		# not enough constraints solved
		if len(unsolved_beams) > self.structure.dimensions:
			return False

		# underconstrained - take axial component of load
		elif len(unsolved_beams) == 1:
			b = unsolved_beams[0]
			self.tensions[b] = beam_dirs[b].dot(f)

			return True

		# build a matrix with the columns as unsolved beam directions
		unsolved_dirs = [
			beam_dirs[b] for b in unsolved_beams
		]

		# underconstrained - take components of load within the plane
		if len(unsolved_dirs) == 2 and self.structure.dimensions == 3:
			a, b = unsolved_dirs
			unsolved_dirs.append(np.cross(a, b))

		unsolved_dir_matrix = np.array(unsolved_dirs).T

		# solve
		try:
			tensions = -np.linalg.solve(unsolved_dir_matrix, f)
		except np.linalg.LinAlgError:
			# underconstrained
			return False

		for beam, tension in zip(unsolved_beams, tensions):
			self.tensions[beam] = tension

		return True
