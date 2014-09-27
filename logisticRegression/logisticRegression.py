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
	
	# plt.figure ('normal Logistic gradient descent for iteration of 500 times')
	# weight = gradientDescent (train_x , train_y , {'alpha' : 0.01 , 'maxIteration' : 500 , 'optimizeType' : 'gradDescent'})
	
	# plt.figure ('normal gradient descent for iteration of 500 times')
	# weight = gradientDescent (train_x , train_y , {'alpha' : 0.001 , 'maxIteration' : 500 , 'optimizeType' : 'gradDescent'})
	
	# plt.figure ('randowm gradient descent')
	# weight = gradientDescent (train_x , train_y , {'alpha' : 0.01 , 'maxIteration' : 500 , 'optimizeType' : 'randomGradDescent'})
	
	plt.figure ('smooth randowm gradient descent')
	weight = gradientDescent (train_x , train_y , {'alpha' : 0.01 , 'maxIteration' : 500 , 'optimizeType' : 'smoothRandomGradDescent'})
	
	xClassOne , yClassOne = [] , []
	xClassTwo , yClassTwo = [] , []
	for i in range (cntSample) :
		if train_y[i] == 0 :
			xClassOne.append (train_x[i , 1])
			yClassOne.append (train_x[i , 2])
		else :
			xClassTwo.append (train_x[i , 1])
			yClassTwo.append (train_x[i , 2])

	min_x = min (train_x[: , 1])[0 , 0]
	max_x = max (train_x[: , 1])[0 , 0]
	classOne = plt.plot (xClassOne , yClassOne , 'or' , label = 'classOne')
	classTwo = plt.plot (xClassTwo , yClassTwo , 'ob' , label = 'classTwo')

	# w0 * 1 + w1 * x1 + w2 * x2 = 0 -> x2 = (-w0 - w1 * x1) / w2
	weight = weight.T
	min_y = float (-weight[0 , 0] - weight[0 , 1] * min_x) / weight[0 , 2]
	max_y = float (-weight[0 , 0] - weight[0 , 1] * max_x) / weight[0 , 2]

	border = plt.plot ([min_x , max_x] , [min_y , max_y] , '-g' , label = 'border')
	plt.xlabel('X1') 	
	plt.ylabel('X2')  

	plt.legend ()
	plt.show ()     
	return weight.T

def testLogistic (test_x , test_y , weight) :
	cntSample , cntFeature = shape (test_x)
	cntMatch = 0
	for i in range (cntSample) :
		if (sigmod (test_x[i , :] * weight)[0 , 0] > 0.5) == bool (test_y[i , 0]) :
			cntMatch += 1
	return cntMatch * 1.0 / cntSample