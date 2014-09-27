#-*-coding:utf-8-*-
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

def sigmod (num) :
	return 1.0 / (1 + exp (-num));

def gradientDescent (train_x , train_y , operation) :
	startTime = time.time ()
	cntSample , cntFeature = shape (train_x)
	alpha = operation['alpha']
	maxIteration = operation['maxIteration']
	weight = ones ((cntFeature , 1))
	if operation['optimizeType'] == 'gradDescent' :
		#normal gradient descent algorithm
		for cntIteration in range (maxIteration) :
			get_y = sigmod (train_x * weight)
			error = (get_y - train_y)
			weight = weight - alpha * train_x.T * error
	elif operation['optimizeType'] == 'randomGradDescent' :
		#random gradient descent algorithm
		for i in range (cntSample) :
			get_y = sigmod (train_x[i , :] * weight)
			error = (get_y - train_y[i , 0])
			weight = weight - alpha * train_x[i , :].T * error
	elif operation['optimizeType'] == 'smoothRandomGradDescent' :
		#smooth random gradident descent algorithm
		for cntIteration in range (maxIteration) :
			dataIndex = range (cntSample)
			for i in range (cntSample) :
				alpha = 4.0 / (1 + cntIteration + i) + 0.01
				randInt = int (random.uniform (0 , len (dataIndex)))
				index = dataIndex[randInt]
				gety_y = sigmod (train_x[index , :] * weight)
				error = (gety_y - train_y[index , 0])
				weight = weight - alpha * train_x[index , :].T * error
				del (dataIndex[randInt])

	print 'Congratulations, training complete! Took %fs!' % (time.time() - startTime) 
	print 'the final error for train set is %f!' % (sum (square ((sigmod (train_x * weight) - train_y))) / 2.0)
	return weight
			
def showLogistic (train_x , train_y) :
	cntSample , cntFeature = shape (train_x)

	weight = gradientDescent (train_x , train_y , {'alpha' : 0.01 , 'maxIteration' : 500 , 'optimizeType' : 'gradDescent'})
	return weight

def testLogistic (test_x , test_y , weight) :
	cntSample , cntFeature = shape (test_x)
	cntMatch = 0
	for i in range (cntSample) :
		if (sigmod (test_x[i , :] * weight)[0 , 0] > 0.5) == bool (test_y[i , 0] - 1.0) :
			cntMatch += 1
	return cntMatch * 1.0 / cntSample