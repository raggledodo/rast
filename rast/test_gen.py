''' Test rast generator '''

import re
import unittest

from rast.last import node
from rast.plugin import setBuilder, _defaultBuilder
from rast.ast import term, nonterm
from rast.gen import generator

TERMS = [
	term('LEAF', 'type1'),
	term('LEAF2', 'type2'),
]
NTERMS = [
	nonterm('OP', {
		'type1': [
			['type1', 'type1'],
			['type1', 'type2'],
		],
		'type2': [
			['type2', 'type1'],
			['type2', 'type2'],
		]
	}, attr={}),
	nonterm('TWICE', {
		'type1': [['type2']],
		'type2': [['type1']],
	}, attr={'limit': 2})
]

# bottom up traverse utility
def _traverse(root, func, depth=0):
	if root.inputs:
		for arg in root.inputs:
			_traverse(arg, func, depth+1)
		func(root, depth)

class mockNode(node):
	def __init__(self, name, otype, parent, i, attr={}):
		super(mockNode, self).__init__(name, otype, parent, i, attr)
		self.parent = parent
		self.attr = attr
		if parent:
			self.otype = parent.itypes[i]

def setMock():
	setBuilder(lambda name, itypes, parent, i, attr: \
		mockNode(name, itypes, parent, i, attr))

class TestGen(unittest.TestCase):
	def test_rtree(self):
		def typecheck(node, depth):
			itypes = list(map(lambda i: i.otype, node.inputs))
			for expect_it, got_it in zip(node.itypes, itypes):
				self.assertEqual(expect_it, got_it)
		
		setMock()
		g = generator(TERMS, NTERMS, (3, 10)) 

		for i in range(1000):
			root = g.randTree()
			_traverse(root, typecheck)

	def test_depth(self):
		mdepth = {"depth": 0}
		def depthcheck(node, depth):
			mdepth["depth"] = max(mdepth["depth"], depth)

		setMock()
		g = generator(TERMS, NTERMS, (3, 10))

		for i in range(1000):
			root = g.randTree()
			_traverse(root, depthcheck)
			self.assertLessEqual(3, mdepth["depth"])
			self.assertGreaterEqual(10, mdepth["depth"])
			mdepth["depth"] = 0

	def test_limit(self):
		setBuilder(_defaultBuilder)
		g = generator(TERMS, NTERMS, (3, 10))

		for i in range(1000):
			root = g.randTree()
			twices = [m.start() for m in re.finditer('TWICE', str(root))]
			self.assertGreater(3, len(twices))
