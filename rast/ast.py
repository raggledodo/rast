''' AST (template definition) '''

import random

from rast.plugin import safeNode

# leaf template
class term(object):
	def __init__(self, name, otype):
		'''
		name 	string
		otype 	string
		'''
		self.name = name
		self.otype = otype
	
	def create(self, parent, i):
		'''
		parent 	node
		i 		int
		return node
		'''
		out = safeNode(self.name, [self.otype], parent, i)
		return out

# operational template
class nonterm(object):
	def __init__(self, name, otype, attr):
		'''
		name 	string
		otype 	dict<string: [][]string>
		attr: 	dict
		'''
		isinstance(otype, dict)
		self.name = name
		self.attr = attr
		self.uses = 0
		for oname in otype:
			itypes = otype[oname]
			assert isinstance(itypes, list) and len(itypes) > 0 and isinstance(itypes[0], list)
		self.tinfos = otype

	def create(self, parent, i, otype):
		'''
		parent 	node
		i 		int
		otype 	string
		return node
		'''
		assert otype in self.tinfos
		self.uses = self.uses+1
		out = safeNode(self.name, random.choice(self.tinfos[otype]), 
			parent, i, self.attr)
		return out
