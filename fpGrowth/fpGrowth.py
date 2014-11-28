
class treeNode :
	"""
	"""
	def __init__ (self , name , count , pre) :
		self.name = name
		self.count = count
		self.nextNode = None
		self.fatherNode = pre
		self.child = {}
	
	def inc (self , count) :
		self.count += count
	
	def display (self , dep = 1) :
		print ' ' * dep , self.name , ' ' , self.count
		for each in self.child :
			self.child[each].display (dep + 1)

def creatInitData (dataSet) :
	"""
	"""
	data = {}
	for each in dataSet :
		data[frozenset (each)] = 1 
	return data

def creatFpTree (dataSet , minSupport) :
	"""
	"""
	headerTable = {}
	for each in dataSet :
		for item in each :
			headerTable[item] = headerTable.get (item , 0) + dataSet[each]
	for each in headerTable.keys () :
		if headerTable[each] < minSupport :
			del (headerTable[each])
	frequentItem = set (headerTable.keys())
	if len (frequentItem) == 0:
		return None , None
	for each in frequentItem :
		headerTable[each] = [headerTable[each] , None]
	treeRoot = treeNode ('tree root' , 1 , None)
	for each , count in dataSet.items () :
		localCount = {}
		for item in each :
			if item in frequentItem :
				localCount[item] = headerTable[item]
		if len (localCount) > 0 :
			orderItem = [v[0] for v in sorted (localCount.items() , key = lambda p : (p[1][0] , p[0]) , reverse = True)]
			updateTree (orderItem , treeRoot , headerTable , count)
	return treeRoot , headerTable

def updateTree (items , tree , headerTable , count) :
	"""
	"""
	if items[0] in tree.child :
		tree.child [items[0]].inc (count)
	else :
		tree.child [items[0]] = treeNode (items[0] , count , tree)
		if headerTable[items[0]][1] == None :
			headerTable[items[0]][1] = tree.child [items[0]]
		else :
			updateHeader (headerTable[items[0]][1] , tree.child [items[0]])
	
	if len (items) > 1 :
		updateTree (items[1:] , tree.child [items[0]] , headerTable , count)

def updateHeader (node , target) :
	"""
	"""
	while node.nextNode != None :
		node = node.nextNode
	node.nextNode = target
	
def ascendTree (node , path) :
	"""
	"""
	if node.fatherNode != None :
		path.append (node.name)
		ascendTree (node.fatherNode , path)

def findPrePath (base , node) :
	"""
	"""
	prePath = {}
	while node != None :
		path = []
		ascendTree (node , path)
		if len (path) > 1 :
			prePath [frozenset (path[1:])] = node.count
		node = node.nextNode
	return prePath

def fpGrowth (tree , headerTable , minSupport , prePath , frequentList) :
	"""
	"""
	local = [v[0] for v in sorted (headerTable.items() , key = lambda p : p[1])]
	for each in local :
		newFreq = prePath.copy ()
		newFreq.add (each)
		frequentList.append (newFreq)

		conditionData = findPrePath (each , headerTable[each][1])
		newTree , newHead = creatFpTree (conditionData , minSupport)

		if newHead != None :
			fpGrowth (newTree , newHead , minSupport , newFreq , frequentList)



