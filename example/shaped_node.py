''' lAST extension allowing shape '''

import random
import numpy as np

from rast.last import node
from rast.plugin import setBuilder

MIN_RANK = 0
MAX_RANK = 6

def expand(shape, idx, mul):
	after = shape[idx:]
	out = shape[:idx]
	out.append(mul)
	out.extend(after)
	return out

def ELEM(node):
	for arg in node.inputs:
		arg.shape = node.shape

def REDUCE(node):
	shape = node.shape
	rank = len(shape)
	if len(node.inputs) > 1:
		limit = rank + 1
		idx = random.randint(0, rank)
		mul = random.randint(1, 9)
		node.inputs[0].shape = expand(shape, idx, mul)
		node.inputs[1].shape = [1] 
		node.inputs[1].scalar = idx
	else:
		node.inputs[0].shape = list(np.random.randint(1, high=9, size=random.randint(1, rank)))

def MATMUL(node):
	assert len(node.inputs) == 2
	shape = node.shape
	if len(shape) < 2:
		shape = [shape[0], 1]
	common = random.randint(1, 9)
	if len(shape) > 2:
		beyond = shape[:-2]
	else:
		beyond = []
	node.inputs[0].shape = beyond + [shape[-2], common]
	node.inputs[1].shape = beyond + [common, shape[-1]]

SHAPER = {
	'ELEM': ELEM,
	'REDUCE': REDUCE,
	'MATMUL': MATMUL
}

class shapeNode(node):
	def __init__(self, *args, **kwargs):
		super(shapeNode, self).__init__(*args, **kwargs)
		self.shape = None
		self.scalar = None

	def __repr__(self):
		s = super(shapeNode, self).__repr__()
		if self.scalar:
			s = s + "<%d>" % self.scalar
		else:
			s = s + "[%s]" % str(self.shape)
		return s

	def plugin(self, parent, i, attr={}):
		if parent is None:
			self.shape = list(np.random.randint(2, high=9, size=random.randint(MIN_RANK, MAX_RANK)))
		SHAPER[attr['shape']](self)

setBuilder(lambda name, itypes: shapeNode(name, itypes))
