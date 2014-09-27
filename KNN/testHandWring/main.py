from numpy import *
import operator
import os
from KNN import *

def getData (file) :
	"""
	get the data from file
	the data in file is a Matrix of 32 * 32
	convert the matrix to vector
	"""
	# 1024 = 32 * 32
	data = zeros ((1 , 1024))
	inputFile = open (file)
	for row in range (32) :
		lineStr = inputFile.readline ()
		for col in range (32) :
			data[0][row * 32 + col] = int (lineStr[col])
	return data

def loadDataSet () :
	"""
	load the data , including the trainData & testData
	"""
	dataDir = r'E:/Python/KNN/'
	print 'Getting Trainging Data'
	trainFileList = os.listdir (dataDir + 'trainingDigits')
	cntTrain = len (trainFileList)
	train_data = zeros ((cntTrain , 1024))
	train_number = []
	for i in range (cntTrain):
		fileNmae = trainFileList[i]
		# get the features of data
		train_data[i , :] = getData (dataDir + 'trainingDigits/' + fileNmae)
		# get the classname it belong to
		train_number.append (fileNmae.split ('_')[0])

	print 'Getting Testing Data'
	testFileList = os.listdir (dataDir + 'testDigits')
	cntTest = len (testFileList)
	test_data = zeros ((cntTest , 1024))
	test_number = []
	for i in range (cntTest) :
		fileNmae = testFileList[i]
		test_data[i , :] = getData (dataDir + 'testDigits/' + fileNmae)
		test_number.append (fileNmae.split ('_')[0])
	print 'loadDataSet over'
	return train_data , train_number , test_data , test_number

def testHandWriting () :
	"""
	test the kNNClassify
	for eatch testData , predict the class it belong to
	then check its accuracy
	"""
	print 'step 1 : load dataSet ...'
	train_data , train_number , test_data , test_number = loadDataSet ()
	print 'step 2 : training ...'
	cntTest = len (test_number)
	print 'step 3 : testing ...'
	correct = 0.0
	for i in range (cntTest) :
		# get the predict result
		indexClassify = kNNClassify (train_data , test_data[i , :] , train_number , 3)
		# check its correctness
		if indexClassify == test_number[i] :
			correct += 1
	print 'step 4 : calculate the result ...'
	print 'The classify accuracy is %.2f%%' % (float(correct * 100) / float (cntTest))

if __name__ == '__main__' :
	testHandWriting ();