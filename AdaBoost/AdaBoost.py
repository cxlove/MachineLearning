from weakCluster import *
from numpy import *

def adaBoostTrain (dataSet , labels , numIter = 40) :
	"""
	"""
	n , m = dataSet.shape
	D = mat (ones ((n , 1)) / n)
	cluster = []
	predictClass = mat (zeros ((n , 1)))
	for i in range (numIter) :
		bestStump , predict , error = buildStump (dataSet , labels , D)
		alpha = float (0.5 * log ((1 - error) / max (error , 1e-15)))
		bestStump['alpha'] = alpha
		cluster.append (bestStump)
		temp = multiply (-1.0 * alpha * labels , predict)
		D = multiply (D , exp (temp))
		D = D / D.sum ()

		predictClass += alpha * predict
		predictError = multiply (sign (predictClass) != labels , ones ((n , 1)))
		errorRate = predictError.sum() / n
		
		print "Iteration " , i , " : " , errorRate
		if errorRate == 0.0 :
			break
	return cluster

def adaBoostTest (dataSet , labels , cluster) :
	"""
	"""
	n , m = dataSet.shape 
	predictClass = mat (zeros ((n , 1)))
	for i in range (len (cluster)) :
		stump = cluster[i]
		predict = stumpClassify (dataSet , stump['feature'] , stump['value'] , stump['symbol'])
		predictClass += predict * stump['alpha']
	
	error = multiply (sign (predictClass) == labels , ones ((n , 1)))
	return error.sum () * 1.0 / n
