''' Less Abstract ST (working node abstract class) '''

# working node representation generated
class node(object):
	def __init__(self, name, itypes):
		self.name = name
		self.itypes = itypes
		self.inputs = None

	def __repr__(self):
		if self.inputs:
			postfix = '(' + str(self.inputs) + ')'
		else:
			postfix = ''
		return self.name + postfix

	# abstract method for extension
	# should apply to self with attr
	def plugin(self, parent, i, attr={}):
		pass
