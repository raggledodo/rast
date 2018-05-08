''' Less Abstract ST (working node abstract class) '''

# working node representation generated
class node(object):
	def __init__(self, name, itypes, 
		parent=None, i=0, attr={}):
		'''
		name 	string
		itypes 	[]string
		parent 	node
		i 		int
		attr 	dict
		'''
		self.name = name
		self.itypes = itypes
		self.inputs = None

	def __repr__(self):
		if self.inputs:
			postfix = '(' + str(self.inputs) + ')'
		else:
			postfix = ''
		return self.name + postfix
