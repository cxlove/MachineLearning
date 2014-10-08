from numpy import *

def stumpClassify (dataSet , feature , value , inequalSymbol) :
	"""
	for the decision condition (feature , value , inequalSymbol)
	classify the dataSet
	inequalSymbol : 'small' : <=  , 'large' : >
	"""
	n , m = dataSet.shape
	labels = ones ((n , 1))
	if inequalSymbol == 'small' :
		labels[dataSet[: , feature] > value] = -1
	else :
		labels[dataSet[: , feature] <= value] = -1
	return labels

def buildStump (dataSet , labels , D) :
	"""
	decision tree , only have one decision condition
	just a stump
	"""
	n , m = dataSet.shape
	minError = 1e60
	bestStump = {}
	bestClassify = mat (zeros ((n , 1)))
	for feature in range (m) :
		for i in range (n) :
			value = dataSet[i , feature]
			for symbol in ['small' , 'large'] :
				predict = stumpClassify (dataSet , feature , value , symbol)
				error = mat (ones ((n , 1)))
				error[predict == labels] = 0
				weightError = D.T * error
				if weightError < minError :
					minError = weightError
					bestStump['feature'] = feature
					bestStump['value'] = value
					bestStump['symbol'] = symbol
					bestClassify = predict.copy ()
	return bestStump , bestClassify , minError



	
