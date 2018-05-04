''' Test abstract syntax tree template '''

import unittest

from rast.last import node
from rast.plugin import setBuilder
from rast.ast import term, nonterm

PARENT_NAME = 'sample_parent'
PARENT_ITYPES = ['parent_itype']
PARENT = node(PARENT_NAME, PARENT_ITYPES)

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

class TestAST(unittest.TestCase):
	def test_term(self):
		CHILD_NAME = 'sample_leaf'
		CHILD_OTYPE = 'sample_outtype'

		setMock()
		temp = term(CHILD_NAME, CHILD_OTYPE)
		child = temp.create(PARENT, 0)
		self.assertTrue(isinstance(child, node))
		self.assertTrue(isinstance(child, mockNode))

		self.assertEqual(CHILD_NAME, child.name)
		self.assertEqual([CHILD_OTYPE], child.itypes)
		self.assertEqual(0, len(child.attr))
		self.assertIs(PARENT, child.parent)

	def test_nterm(self):
		PARENT2_NAME = 'sample_parent2'
		PARENT2_ITYPE = 'literal_itype'
		EXPECT_ITYPES = [['sample_itype', 'sample_itype2']]
		PARENT2 = node(PARENT2_NAME, [PARENT2_ITYPE])
		EXPECT2_ITYPES = [['abcd']]
		CHILD_NAME = 'sample_leaf'
		CHILD_OTYPES = {
			PARENT_ITYPES[0]: EXPECT_ITYPES,
			'noparent_itype': [['sample_itype3']],
		}
		CHILD_ATTR = {'key': 'value'}
		parent = node(PARENT_NAME, PARENT_ITYPES)

		setMock()
		temp = nonterm(CHILD_NAME, CHILD_OTYPES, CHILD_ATTR)
		child = temp.create(PARENT, 0, PARENT.itypes[0])
		self.assertTrue(isinstance(child, node))
		self.assertTrue(isinstance(child, mockNode))

		self.assertEqual(CHILD_NAME, child.name)
		self.assertEqual(EXPECT_ITYPES[0], child.itypes)
		self.assertEqual(PARENT_ITYPES[0], child.otype)
		self.assertIs(CHILD_ATTR, child.attr)
		self.assertIs(PARENT, child.parent)
