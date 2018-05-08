''' Generate random nodes '''

import math
import random

from rast.ast import term, nonterm

# create random node tree
class generator(object):
	def __init__(self, terms, nterms, depths):
		'''
		terms 	[]term
		nterms 	[]nonterms
		depths 	(int, int)
		'''
		self.terms = terms
		self.nterms = nterms
		self._mindepth, self._maxdepth = depths
		assert self._maxdepth > self._mindepth
		assert self._mindepth >= 0

	def randTree(self, parent=None, i=0, depth=0):
		'''
		parent 	node
		i 		int
		depth 	int
		return node
		'''
		filtLeaf = self.terms
		filtOp = self.nterms
		if depth > 0 or parent is not None:
			otype = parent.itypes[i]
			# select appropriate nodes to choose from
			filtLeaf = list(filter(lambda leaf: otype == leaf.otype, filtLeaf))
			filtOp = list(filter(lambda op: otype in op.tinfos, filtOp))
			filtOp = list(filter(lambda op: 'limit' not in op.attr or
				op.uses < op.attr['limit'], filtOp))
		else:
			otype = None

		if depth < self._mindepth:
			prTerm = 0.0
		else:
			prTerm = math.sqrt(float(depth - self._mindepth) / 
				(self._maxdepth - self._mindepth))
		stop = random.uniform(0, 1) < prTerm

		if stop and len(filtLeaf) > 0 or len(filtOp) == 0: # if terminating and leaf available
			leafTerm = random.choice(filtLeaf)
			assert isinstance(leafTerm, term)
			root = leafTerm.create(parent, i)
		else: # always fallback to available operations
			opTerm = random.choice(filtOp)
			assert isinstance(opTerm, nonterm)
			if not otype:
				otype = random.choice(list(opTerm.tinfos.keys()))
			root = opTerm.create(parent, i, otype)
			root.inputs = [self.randTree(parent=root, i=i, depth=depth+1) 
				for i in range(len(root.itypes))]

		return root
