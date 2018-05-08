''' Add builder function for extended last.node '''

from rast.last import node

def _defaultBuilder(name, itypes,
	parent=None, i=0, attr={}):
	return node(name, itypes)

_builder = _defaultBuilder

def setBuilder(builder):
	'''
	builder 	func(string, []string, node, int, dict)node
	'''
	global _builder
	_builder = builder

def safeNode(name, itypes,
	parent=None, i=0, attr={}):
	'''
	name 		string
	itypes 		[]string
	parent		node
	i 			int
	attr		dict
	return node
	'''
	out = _builder(**locals())
	assert isinstance(out, node)
	return out
