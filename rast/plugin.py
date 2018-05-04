''' Add builder function for extended last.node '''

from rast.last import node

def _defaultBuilder(name, itypes,
	parent=None, i=0, attr={}):
	return node(name, itypes)

_builder = _defaultBuilder

def setBuilder(builder):
	global _builder
	_builder = builder

def safeNode(name, itypes,
	parent=None, i=0, attr={}):
	out = _builder(**locals())
	assert isinstance(out, node)
	return out
