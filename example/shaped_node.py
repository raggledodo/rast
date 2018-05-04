''' lAST extension allowing shape '''

import random
import numpy as np

from rast.last import node
from rast.plugin import setBuilder

def expand(shape, idx, mul):
	after = shape[idx:]
	out = shape[:idx]
	out.append(mul)
	out.extend(after)
	return out

def ELEM(node):
	for arg in node.inputs:
		arg.shapeinit(node.shape)

def REDUCE(node):
	shape = node.shape
	rank = len(shape)
	if len(node.inputs) > 1:
		limit = rank + 1
		idx = random.randint(0, rank)
		mul = random.randint(1, 9)
		node.inputs[0].shapeinit(expand(shape, idx, mul))
		node.inputs[1].shapeinit([1], idx)
	else:
		node.inputs[0].shapeinit(
			list(np.random.randint(1, high=9, size=random.randint(1, rank))))

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
	node.inputs[0].shapeinit(beyond + [shape[-2], common])
	node.inputs[1].shapeinit(beyond + [common, shape[-1]])

SHAPER = {
	'ELEM': ELEM,
	'REDUCE': REDUCE,
	'MATMUL': MATMUL
}

class shapeNode(node):
	def __init__(self, name, itypes, 
		parent=None, i=0, attr={}):
		super(shapeNode, self).__init__(**locals())
		self.shapeLabel = attr['shape']
		self.shape = None
		self.scalar = None

	def __repr__(self):
		s = super(shapeNode, self).__repr__()
		if self.scalar:
			s = s + "<%d>" % self.scalar
		else:
			s = s + "[%s]" % str(self.shape)
		return s

	def shapeinit(self, shape, scalar=None):
		self.shape = shape
		self.scalar = scalar
		SHAPER[self.shapeLabel](self)

setBuilder(lambda name, itypes, parent, i, attr: \
	shapeNode(name, itypes, parent, i, attr))
