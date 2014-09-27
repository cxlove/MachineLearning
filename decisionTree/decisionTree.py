#-*-coding:utf-8-*-
from math import *

def calcShannonEnt (dataSet) :
	"""
	calculate the information gain and entropy
	H = - \sum_{i = 1}^{n}p(x_i)\log_{2}p(x_i) 
	"""
	numEntries = len (dataSet)
	labelDict = {}
	for featureVec in dataSet :
		label = featureVec[-1]
		if label not in labelDict.keys() :
			labelDict[label] = 0
		labelDict[label] += 1

	shannonEntropy = 0.0
	for key in labelDict :
		p_i = float (labelDict[key]) / numEntries
		shannonEntropy += p_i * log (p_i , 2)
	return -shannonEntropy

def majorityClass (classList) :
	"""
	choss the major class
	"""
	classCount = {}
	for vote in classList :
		if vote not in classCount.keys () :
			classCount[vote] = 0
		classCount[vote] += 1
	sortedClass = sorted (classCount.iteritems () , key = operator.itemgetter(1) , reverse = True)
	return sortedClass[0][0]

def splitDataSet (dataSet , feature , value) :
	"""
	split th dataSet by the (feature : value)
	"""
	subDataSet = []
	for featureVec in dataSet :
		if featureVec[feature] == value :
			# erase the feature
			newFeatureVec = featureVec[ : feature]
			newFeatureVec.extend (featureVec[feature + 1 : ])
			subDataSet.append (newFeatureVec)
	return subDataSet

def chooseBestFeatureSplit (dataSet) :
	"""
	enumerate all the feature
	choose the best feature to split the dataSet by the minimum of shannon entropy
	"""
	bestFeature = -1
	bestEntropy = -1.0
	baseEntropy = calcShannonEnt (dataSet)
	numData = len (dataSet)
	numFeature = len (dataSet[0]) - 1
	for i in range (numFeature) :
		featureValue = set ([example[i] for example in dataSet])
		nowEntropy = 0.0
		for value in featureValue :
			subDataSet = splitDataSet (dataSet , i , value)
			prob = (float)(len (subDataSet)) / numData
			nowEntropy += prob * calcShannonEnt (subDataSet)
		if baseEntropy - nowEntropy > bestEntropy :
			bestEntropy = baseEntropy - nowEntropy
			bestFeature = i
	return bestFeature

def buildTree (dataSet , labels) :
	"""
	creat the decision tree
	"""
	# all the data belong to one class
	classList = [example[-1] for example in dataSet]
	if classList.count (classList[0]) == len (classList) :
		return classList[0]
	# have no feature to classify , so choose the major class
	if len (dataSet[0]) == 1 :
		return majorityClass (classList)
	bestFeature = chooseBestFeatureSplit (dataSet)
	bestFeatureLabel = labels[bestFeature]
	tree = {bestFeatureLabel : {}}
	del (labels[bestFeature])
	featureValue = set ([example[bestFeature] for example in dataSet])
	for value in featureValue :
		subLabels = labels[:]
		tree[bestFeatureLabel][value] = buildTree (splitDataSet (dataSet , bestFeature , value) , subLabels)
	return tree

def loadData () :
	# dataSet = [[1 , 1 , 'yes'] , [1 , 1 , 'yes'] , [1 , 0 , 'no'] , [0 , 1 , 'no'] , [0 , 0 , 'no']]
	# labels = ['no surfacing' , 'flippers']
	# return dataSet , labels

	fileAddress = 'E:/Python/decisionTree/input.txt'
	file = open (fileAddress)
	data = file.readlines ()
	allRow = len (data)
	row = 0
	featureCnt , row = int (data[row]) , row + 1
	labels = []
	dataSet = []
	feature = []
	for i in range (featureCnt + 1) :
		feature.append (data[row].strip().split ('\t'))
		if i < featureCnt :
			labels.append (feature[-1][0])
		row += 1
	while row < allRow :
		line = map (int , data[row].strip ().split ())
		row += 1
		for i in range (1 , len (line)) :
			line[i] = feature[i - 1][line[i]]
		dataSet.append (line[1 : ])
	return dataSet , labels

def mainProcess () :
	dataSet , labels = loadData ();
	return buildTree (dataSet , labels)
