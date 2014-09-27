from numpy import *

def kNNClassify (trainData , testData , labels , k) :
	"""
	trainData : N * M , n training data , each of them have m data
	testData : 1 * M
	labels : correspond to the trainData , witch class it belong to
	k : number of neighbors to use for classify
	"""
	cntDataSet = trainData.shape[0]
	# tite --- copy cntDataSet times , 1 * M -> N * M
	diff = (tile (testData , (cntDataSet , 1)) - trainData) ** 2
	distSortedId = argsort (sum (diff , axis = 1))
	# dict , cal the times for each class
	classCount = {}
	for i in range (min (k , cntDataSet)) :
		index = labels[distSortedId[i]]
		classCount[index] = classCount.get (index , 0) + 1
	# the testData belong to the class which have maximum times
	maxCount , maxIndex = -1 , -1
	for key , value in classCount.items () :
		if value > maxCount :
			maxCount , maxIndex = value , key
	return maxIndex