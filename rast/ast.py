''' AST (template definition) '''

import random

from rast.plugin import safeNode

# leaf template
class term:
	def __init__(self, name, otype):
		self.name = name
		self.otype = otype
	
	def create(self, parent, i):
		out = safeNode(self.name, [self.otype])
		out.plugin(parent, i)
		return out

# operational template
class nonterm:
	def __init__(self, name, otype, attr):
		isinstance(otype, dict)
		self.name = name
		self.attr = attr
		self.uses = 0
		for oname in otype:
			itypes = otype[oname]
			assert isinstance(itypes, list) and len(itypes) > 0 and isinstance(itypes[0], list)
		self.tinfos = otype

	def create(self, parent, i, otype):
		assert otype in self.tinfos
		self.uses = self.uses+1
		out = safeNode(self.name, random.choice(self.tinfos[otype]))
		out.plugin(parent, i, self.attr)
		return out
