#-*-coding:utf-8-*-
# author : cxlove

import random
import time
from numpy import *
import matplotlib.pyplot as plt

class SVMStruct :
	"""
	the struct of SVM
	"""
	def __init__ (self , train_x , train_y , C , toleration , kernelOption) :
		self.train_x = train_x          # feature of the dataSet
		self.train_y = train_y          # label of the dataSet
		self.C = C                      # slack variable
		self.toleration = toleration    # termination codition
		self.numSample , self.numFeature = shape (train_x)
		self.alpha = mat (zeros ((self.numSample , 1)))
		self.kernelOption = kernelOption
		self.kernelMatrix = calKernelMatrix (train_x , kernelOption) # K(i , j)
		self.b = 0
		self.E = mat (zeros ((self.numSample , 2)))

def calError (svm , j) :
	"""
	w = \sum_{i=1}^N\alpha_iy_ix_i
	e[j] = (w*x_j+b)-y_j	
	"""
	return (multiply (svm.alpha , svm.train_y).T * svm.kernelMatrix[: , j] + svm.b) - svm.train_y[j , 0]

def updateError (svm , i) :
	"""
	"""
	error = calError (svm , i)
	svm.E[i] = [1 , error]

def calKernel (xi , x , kernelOption) :
	"""
	for each x_j in x : calculate the K(x_i , x_j)
	"""
	n , m = shape (x)
	kernel = mat (zeros ((n , 1)))
	if kernelOption[0] == 'linear' :
		# print xi , x
		kernel = x * xi.T
	elif kernelOption[0] == 'rbf' : 
		sigma = kernelOption[1]
		for i in range (n) :
			# K(x , y) = exp (\frac {-||x - y|| ^ 2}{\sigma ^ 2})
			diff = xi - x[i , :]
			kernel[i] = exp (-1.0 * (diff * diff.T) / (2 * sigma ** 2))
	else :
		print 'error : no such kernelOption'
	return kernel

def calKernelMatrix (x , kernelOption) :
	"""
	calculate the kernel matrix
	n * n for each pair of vector (x_i , x_j)
	"""
	n , m = shape (x)
	matrix = mat (zeros ((n , n)))
	for i in range (n) :
		matrix[: , i] = calKernel (x[i , :] , x , kernelOption)
	return matrix

def chooseAlpha2 (svm , alpha_1 , error_1) :
	"""
	"""
	svm.E[alpha_1] = [1 , error_1]
	alpha_2 , error_2 , maxGap = 0 , 0 , 0
	candidate = nonzero (svm.E[: , 0].A)[0]
	if len (candidate) > 1 : 
		for alpha in candidate :
			if alpha == alpha_1 : continue
			error = calError (svm , alpha)
			gap = abs (error - error_1)
			if gap > maxGap :
				maxGap = gap
				alpha_2 = alpha
				error_2 = error
	else :
		alpha_2 = alpha_1
		while alpha_2 == alpha_1 :
			alpha_2 = int (random.uniform (0 , svm.numSample))
		error_2 = calError (svm , alpha_2)
	return alpha_2 , error_2
 

def innerLoop (svm , alpha_1) :
	"""
	"""
	error_1 = calError (svm , alpha_1)
	# print alpha_1 , error_1
	#KKT codition
	# y_i * g(i) <= 1 if alpha_i = C
	# y_i * g(i) >= 1 if alpha_i = 0
	# y_i * g(i) = 1 if 0 < alpha_i < C 

	# check the KKT codition
	if (svm.train_y[alpha_1] * error_1 < -svm.toleration and svm.alpha[alpha_1] < svm.C) or \
		(svm.train_y[alpha_1] * error_1 > svm.toleration and svm.alpha[alpha_1] > 0) :

		# choose alpha_2
		alpha_2 , error_2 = chooseAlpha2 (svm , alpha_1 , error_1) 
		alpha_1_old = svm.alpha[alpha_1].copy ()
		alpha_2_old = svm.alpha[alpha_2].copy ()

		# cal the bound of the alpha_2
		if svm.train_y[alpha_1] == svm.train_y[alpha_2] :
			Low = max (0 , svm.alpha[alpha_1] + svm.alpha[alpha_2] - svm.C)
			High = min (svm.C , svm.alpha[alpha_1] + svm.alpha[alpha_2])
		else :
			Low = max (0 , svm.alpha[alpha_2] - svm.alpha[alpha_1])
			High = min (svm.C , svm.alpha[alpha_2] - svm.alpha[alpha_1] + svm.C)
		if Low == High :
			return False

		k11 = svm.kernelMatrix[alpha_1 , alpha_1]
		k12 = svm.kernelMatrix[alpha_1 , alpha_2]
		k22 = svm.kernelMatrix[alpha_2 , alpha_2]
		eta = 2.0 * k12 - k11 - k22

		if eta >= 0:
			return False

		# update alpha_2
		svm.alpha[alpha_2] -= svm.train_y[alpha_2] * (error_1 - error_2) / eta

		# clip alpha_2
		if svm.alpha[alpha_2] <= Low :
			svm.alpha[alpha_2] = Low
		if svm.alpha[alpha_2] >= High :
			svm.alpha[alpha_2] = High

		if abs (svm.alpha[alpha_2] - alpha_2_old) < 0.00001 :
			updateError (svm , alpha_2)
			return False

		# update the alpha_1 according to the optimize of the alpha_1
		svm.alpha[alpha_1] += svm.train_y[alpha_1] * svm.train_y[alpha_2] *\
			(alpha_2_old - svm.alpha[alpha_2])

		#update b
		b1 = svm.b - error_1 - svm.train_y[alpha_1] * (svm.alpha[alpha_1] - alpha_1_old) \
													* svm.kernelMatrix[alpha_1, alpha_1] \
							 - svm.train_y[alpha_2] * (svm.alpha[alpha_2] - alpha_2_old) \
							 						* svm.kernelMatrix[alpha_1, alpha_2]  
		b2 = svm.b - error_2 - svm.train_y[alpha_1] * (svm.alpha[alpha_1] - alpha_1_old) \
													* svm.kernelMatrix[alpha_1, alpha_2] \
							 - svm.train_y[alpha_2] * (svm.alpha[alpha_2] - alpha_2_old) \
							 						* svm.kernelMatrix[alpha_2, alpha_2]  
		if svm.alpha[alpha_1] > 0 and svm.alpha[alpha_1] < svm.C :
			svm.b = b1
		elif svm.alpha[alpha_2] > 0 and svm.alpha[alpha_2] < svm.C :
			svm.b = b2
		else : svm.b = (b1 + b2) / 2.0
		updateError (svm , alpha_1)
		updateError (svm , alpha_2)
		# print alpha_1 , alpha_2 , svm.alpha[alpha_1 , 0]  , svm.alpha[alpha_2 , 0]
		return True
	return False

def trainSVM (train_x , train_y , C , toleration , maxIteration , kernelOption) :
	"""
	"""
	svm = SVMStruct (train_x , train_y , C , toleration , kernelOption)

	startTime = time.time ()

	change = False
	entireDataSet = True
	while maxIteration > 0 and (change or entireDataSet) :
		maxIteration -= 1
		change = False
		if entireDataSet :
			# update alpha all over the dataSet
			for i in range (svm.numSample) :
				if innerLoop (svm , i) :
					change = True
		else :
			noBoundData = nonzero ((svm.alpha.A > 0) * (svm.alpha.A < svm.C))[0]
			for i in noBoundData :
				if innerLoop (svm , i) :
					change = True
		if entireDataSet :
			entireDataSet = False
		elif change == False :
			entireDataSet = True
	endTime = time.time ()
	print 'training complete , cost %.5f S' % ((endTime - startTime))
	return svm

def showSVM (svm) :
	"""
	"""
	if svm.numFeature > 2 : 
		print 'error'
		return 

	plt.figure (1)
	for i in range (svm.numSample) :
		if svm.train_y[i] == 1 :
			plt.plot (svm.train_x[i , 0] , svm.train_x[i , 1] , 'or')
		else :
			plt.plot (svm.train_x[i , 0] , svm.train_x[i , 1] , 'ob')

	supportVector = nonzero (svm.alpha.A > 0)[0]

	for i in supportVector:
		plt.plot (svm.train_x[i , 0] , svm.train_x[i , 1] , 'oy')

	w = zeros ((2 , 1))
	for i in supportVector :
		w += multiply (svm.alpha[i] * svm.train_y[i] , svm.train_x[i , :].T)

	# w0 * x0 + w1 * x1 + b = 0
	# x1 = (-b - w0 * x0) / w1

	min_x = min (svm.train_x[: , 0])[0 , 0]
	max_x = max (svm.train_x[: , 0])[0 , 0]
	min_y = float ((-svm.b - w[0] * min_x) / w[1])
	max_y = float ((-svm.b - w[0] * max_x) / w[1])

	# print min_x , min_y
	plt.plot ([min_x , max_x] , [min_y , max_y] , '-g')
	plt.show ()

def testSVM (svm , x , y) :
	"""
	"""
	numSample , numFeature = shape (x)

	# choose the support vector
	supportVectorIndex = nonzero(svm.alpha.A > 0)[0]
	supportVectorAlpha = svm.alpha[supportVectorIndex]
	supportVectorY = svm.train_y[supportVectorIndex]
	supportVectorX = svm.train_x[supportVectorIndex]

	match = 0
	for i in range (numSample) :
		# f(x) = sign (\sum_{i=1}^N\alpha_iy_iK(x , x_i) + b)
		kernel = calKernel (x[i , :] , supportVectorX , svm.kernelOption)
		predict = kernel.T * multiply (supportVectorAlpha , supportVectorY) + svm.b
		if sign (predict) == sign (y[i]) :
			match += 1

	print 'the classify accuracy is %.5f %%' % (match * 100.0 / numSample)
 
