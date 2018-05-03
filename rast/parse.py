''' Parse ast definition '''

import yaml

from rast.gen import generator
from rast.ast import term, nonterm

GROUPS_KEY = 'groups'
LEAVES_KEY = 'leaves'
MINDEPTH_KEY = 'mindepth'
MAXDEPTH_KEY = 'maxdepth'

LEAFTYPE_KEY = 'output'
NAME_KEY = 'names'

OTYPE_KEY = 'outputs'
ATTR_KEY = 'attr'
SUBGROUP_KEY = 'subgroups'

# parses yaml stream and returns generator
def parse(stream):
	raw = yaml.load(stream)

	# manditory parameters
	assert isinstance(raw, dict) and GROUPS_KEY in raw
	groups = _parseGroups(raw[GROUPS_KEY])

	# optional parameters
	if LEAVES_KEY in raw:
		leaves = _parseLeaves(raw[LEAVES_KEY])
	else:
		leaves = None
	if MINDEPTH_KEY in raw:
		mindepth = raw[MINDEPTH_KEY]
	else:
		mindepth = 1
	if MAXDEPTH_KEY in raw:
		maxdepth = raw[MAXDEPTH_KEY]
	else:
		maxdepth = 10

	return leaves, groups, (mindepth, maxdepth)

def _parseLeaves(leaves):
	assert isinstance(leaves, list)
	otypes = []
	return _flatten(list(map(lambda leaf: _parseLeaf(leaf, otypes), leaves)))

def _parseGroups(groups, supergroup={}):
	assert isinstance(groups, list)
	return _flatten(list(map(lambda group: _parseGroup(group, supergroup), groups)))

def _parseLeaf(leaf, otypes):
	assert isinstance(leaf, dict)
	otype = leaf[LEAFTYPE_KEY]
	if otype in otypes:
		raise Exception('duplicate output type %s' % otype)
	names = leaf[NAME_KEY]
	if not isinstance(names, list):
		names = [names]
	return list(map(lambda name: term(name, otype), names))

def _parseGroup(group, supergroup):
	assert isinstance(group, dict)
	if ATTR_KEY in group:
		supergroup[ATTR_KEY] = group[ATTR_KEY]

	if OTYPE_KEY in group:
		supergroup[OTYPE_KEY] = group[OTYPE_KEY]

	if NAME_KEY in group:
		if OTYPE_KEY not in supergroup:
			raise Exception('types not specified group')
		if ATTR_KEY in supergroup:
			attr = supergroup[ATTR_KEY]
		else:
			attr = {}
		otype = supergroup[OTYPE_KEY]
		names = group[NAME_KEY]
		if not isinstance(names, list):
			names = [names]
		for oname in otype:
			itypes = otype[oname]
			if not isinstance(itypes, list):
				itypes = [itypes]
			otype[oname] = list(map(_itypeParse, itypes))
		out = _flatten(list(map(lambda name: nonterm(name, otype, attr), names)))
	elif SUBGROUP_KEY in group:
		out = _flatten(_parseGroups(group[SUBGROUP_KEY], supergroup))
	else:
		raise Exception('no name or subgroup attribute in group')
	return out

def _itypeParse(itype):
	iarr = itype.split(',')
	return list(map(lambda s: s.strip(), iarr))

def _flatten(arr):
	out = []
	if len(arr) == 0:
		pass
	elif isinstance(arr[0], list):
		for a in arr:
			out.extend(a)
	else:
		out = arr
	return out
