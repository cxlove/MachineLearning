
def loadDataSet () :
	"""
	"""
	return [[1 , 3 , 4] , [2 , 3 ,5] , [1 , 2 , 3 , 5] , [2 , 5]]

def creatC1 (dataSet) :
	"""
	"""
	c1 = []
	for data in dataSet :
		for item in data :
			if [item] not in c1 :
				c1.append ([item])
	c1.sort ()
	return map (frozenset , c1)

def scanLimit (dataSet , ck , minSupport = 0.5) :
	"""
	"""
	cnt = {}
	for com in ck :
		for data in dataSet :
			if com.issubset (data) :
				if com not in cnt.keys () :
					cnt[com] = 1
				else : cnt[com] += 1
	numItems = float (len (dataSet))
	retList = []
	supportData = {}
	for key in cnt.keys () :
		value = cnt[key]
		support = value / numItems 
		if support >= minSupport :
			retList.append (key)
		supportData[key] = support
	return retList , supportData

def frequentSubSet (com , lk) :
	"""
	all the subset of com belong to lk
	"""
	for val in com :
		sub = com - set ([val])
		if sub not in lk :
			return False
	return True

def aprioriGen (lk , k) :
	"""
	from (k - 1) to k
	"""
	n = len (lk)
	retList = []
	for i in range (n) :
		for j in range (i + 1 , n ) :
			l1 = list (lk[i])[:k - 2]
			l2 = list (lk[j])[:k - 2]
			l1.sort ()
			l2.sort ()
			if l1 == l2 :
				l = lk[i] | lk[j] 
				if frequentSubSet (l , lk) :
					retList.append (l)
	return retList


def Apriori (dataSet , minSupport = 0.5) :
	"""
	"""
	D = map (set , dataSet)
	c1 = creatC1 (dataSet)
	l1 , supportData = scanLimit (D , c1 , minSupport)
	L = [l1]
	k = 2
	while len (L[k - 2]) > 0 :
		ck = aprioriGen (L[k - 2] , k) 
		lk , supportk = scanLimit (D , ck , minSupport)
		supportData.update (supportk)
		L.append (lk)
		k += 1

	return L , supportData

def generateRule (L , supportData , minConf = 0.7) :
	"""
	"""
	retList = []
	for i in range (1 , len (L)) :
		for freqSet in L[i] :
			H = [frozenset ([item]) for item in freqSet]
			# [1 , 2 , 3] to [set([1]) , set([2]) , set([3])]

			if i > 1 :
				ruleGen (freqSet , H , supportData , retList , minConf)
			else :
				calConf (freqSet , H , supportData , retList , minConf)
	return retList

def calConf (freqSet , H , supportData , retList , minConf) :
	"""
	"""
	can = []
	for seq in H :
		conf = supportData[freqSet] / supportData[freqSet - seq]
		if conf >= minConf :
			can.append (seq)
			retList.append ([freqSet - seq , seq , conf])
			print freqSet - seq , ' -----> ' , seq , '  conf : ' , conf
	return can

def ruleGen (freqSet , H , supportData , retList , minConf) :
	"""
	"""
	k = len (H[0])
	if len (freqSet) > k + 1 :
		tmp = aprioriGen (H , k + 1)
		tmp = calConf (freqSet , tmp , supportData , retList , minConf)
		if len (tmp) > 1 :
			ruleGen (freqSet , tmp , supportData , retList , minConf)
	

