from numpy import *

def euclidSim (A , B) :
	"""
	the euclid distance between A and B
	"""
	return 1.0 / (1.0 + linalg.norm (A - B))

def pearsonSim (A , B) :
	"""
	the pearson correlation between A and B
	"""
	if len (A) < 3 :
		return 1.0
	return 0.5 + 0.5 * corrcoef (A , B , rowvar = 0)[0][1]

def cosSim (A , B) :
	"""
	the cosine similarity between A and B
	sim = \frac{A * B}{||A|| * ||B||}
	"""
	return 0.5 + 0.5 * (float (A.T * B) / (linalg.norm (A) * linalg.norm (B)))

def standEst (dataSet , user , item , calSim) :
	"""
	"""
	n , m = dataSet.shape
	simTotal , ratSimTotal = 0 , 0
	for i in range (m) :
		userRate = dataSet[user , i] 
		if userRate == 0 :
			continue
		overLap = nonzero (logical_and (dataSet[: , item].A > 0 , dataSet[: , i].A > 0))[0]
		if len (overLap) == 0 :
			continue
		sim = calSim (dataSet[overLap , i] , dataSet[overLap , item])
		simTotal += sim
		ratSimTotal += sim * userRate
	
	if simTotal == 0 : simTotal = 1
	return ratSimTotal / simTotal

def getK (sigma) :
	"""
	"""
	sig2 = sigma ** 2
	limit = sum (sig2) * 0.9
	for i in range (len (sigma)) :
		if sum (sig2[: i + 1]) >= limit :
			return i + 1

def svdEst (dataSet , user , item , calSim) :
	"""
	"""
	n , m = dataSet.shape 
	U , Sigma , VT = linalg.svd (dataSet)
	k = getK (Sigma)
	dataZip = dataSet.T * U[:,:k] *  mat (eye (k) * Sigma[:k]).I
	simTotal , ratingTotal = 0 , 0
	for i in range (m) :
		userRating = dataSet[user,i]
		if userRating == 0 : continue
		similarity = calSim (dataZip[item,:].T , dataZip[i,:].T)
		#print 'the %d and %d similarity is %f ' % (item , i , similarity)
		simTotal += similarity
		ratingTotal += similarity * userRating

	if simTotal == 0 : simTotal = 1
	return ratingTotal / simTotal

def recommend (dataSet , user , K = 3 , calSim = pearsonSim , estMethod = standEst) :
	"""
	"""
	unratedItem = nonzero (dataSet[user , :].A == 0)[1]
	if len (unratedItem) == 0 :
		return 'you rated everthing'
	itemScore = []
	for item in unratedItem :
		score = estMethod (dataSet , user , item , calSim) 
		itemScore.append ((item , score))
	return sorted (itemScore , key = lambda j : j[1] , reverse = True)[ : K]



