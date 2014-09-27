def classify (tree , labels , feature) :
	"""
	Recursive in the tree
	"""
	firstVec = tree.keys()[0]
	secondVec = tree[firstVec]
	index = labels.index (firstVec)
	for key in secondVec.keys () :
		if feature[index] == key :
			if type(secondVec[key]).__name__ == 'dict' :
				return classify (secondVec[key] , labels , feature)
			else : return secondVec[key]