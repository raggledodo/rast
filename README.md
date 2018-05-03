# rast

a random abstract syntax tree generator

## design

- plugin 
- generator

trees are constructed on nodes. for random generation purposes, we need to distinguish between terminating (leaf) and non-terminating nodes. If the leaves are indistinguishable from non-terminating nodes, then it's appropriate to represent leaves as some nil, null, or None object. However leaves are often special in terms of AST.

all nodes need to be named
for all nodes, we need to specify output types.
for non-term (operational) nodes, we need to specify possible input types for each output
we need to group multiple names together, since they may share similar identical properties (but have different functions). e.g.: addition and multiplication both take 2 values and return a value of the same type.
