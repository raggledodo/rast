'''
Test rast yaml parser
covers:
- parse.py
'''

import unittest

from rast.parse import parse

NAMES = [
	'ABS',
	'EXP',
	'NEG',
	'SIN',
	'COS',
	'TAN',
	'LOG',
	'SQRT',
	'POW',
	'ADD',
	'MUL',
	'DIV',
	'SUB',
	'RMAX',
	'RSUM',
	'RMAX',
	'RSUM',
	'MATMUL'
]

ATTRS = [
	(13, {'shape': 'ELEM'}),
	(15, {'limit': 1, 'shape': 'REDUCE'}),
	(17, {'shape': 'REDUCE'}),
	(18, {'shape': 'MATMUL'}),
]

TYPES = [
	(2, {'tensor': [['tensor']], 'pneg_tensor': [['pneg_tensor']]}), # UNARY_POS
	(6, {'pneg_tensor': [['tensor']], 'pneg_tensor': [['pneg_tensor']]}), # UNARY_NEG
	(8, {'tensor': [['tensor']]}), # UNARY_NONEG
	(9, { # BINARY_POW
	'tensor': [
		['tensor', 'scalar_d'],
		['tensor', 'tensor'],
		['tensor', 'pneg_tensor'],
		['scalar_d', 'tensor'],
		['scalar_d', 'pneg_tensor']
	],
	'pneg_tensor': [
		['pneg_tensor', 'scalar_d'],
		['pneg_tensor', 'pneg_tensor'],
		['pneg_tensor', 'tensor']
	]
	}),
	(12, { # BINARY_POS
	'tensor': [
		['scalar_d', 'tensor'],
		['tensor', 'scalar_d'],
		['tensor', 'tensor']
	],
	'pneg_tensor': [
		['scalar_d', 'pneg_tensor'],
		['tensor', 'pneg_tensor'],
		['pneg_tensor', 'scalar_d'],
		['pneg_tensor', 'pneg_tensor'],
		['pneg_tensor', 'tensor']
	]
	}),
	(13, { # BINARY_NEG
	'pneg_tensor': [
    	['tensor', 'scalar_d'],
    	['scalar_d', 'tensor'],
    	['tensor', 'tensor'],
    	['pneg_tensor', 'scalar_d'],
    	['scalar_d', 'pneg_tensor'],
    	['pneg_tensor', 'pneg_tensor'],
    	['tensor', 'pneg_tensor'],
    	['pneg_tensor', 'tensor']
	]
	}),
	(15, { # REDUCE
	'tensor': [['tensor', 'scalar_i']],
	'pneg_tensor': [['pneg_tensor', 'scalar_i']]
	}),
	(17, { 'scalar_d': [['tensor'], ['pneg_tensor']]}), # FULLREDUCE
	(18, { 'tensor': [['tensor', 'tensor']] }) # MATMUL
]

class TestParse(unittest.TestCase):
	def test_parse(self):
		with open('example/sample.yaml', 'r') as cfg:
			terms, nterms, (mindepth, maxdepth) = parse(cfg)
			self.assertEqual(2, mindepth)
			self.assertEqual(9, maxdepth)

			self.assertEqual(6, len(terms))
			self.assertEqual('scalar_double', terms[0].name)
			self.assertEqual('scalar_d', terms[0].otype)
			self.assertEqual('scalar_int', terms[1].name)
			self.assertEqual('scalar_i', terms[1].otype)
			self.assertEqual('placeholder', terms[2].name)
			self.assertEqual('tensor', terms[2].otype)
			self.assertEqual('variable', terms[3].name)
			self.assertEqual('tensor', terms[3].otype)
			self.assertEqual('placeholder', terms[4].name)
			self.assertEqual('pneg_tensor', terms[4].otype)
			self.assertEqual('variable', terms[5].name)
			self.assertEqual('pneg_tensor', terms[5].otype)
		
			self.assertEqual(18, len(nterms))

			for i in range(18):
				self.assertEqual(NAMES[i], nterms[i].name)
				j = 0
				while i >= ATTRS[j][0]:
					j = j + 1
				self.assertEqual(ATTRS[j][1], nterms[i].attr)
				k = 0
				while i >= TYPES[k][0]:
					k = k + 1
				self.assertEqual(TYPES[k][1], nterms[i].tinfos)
