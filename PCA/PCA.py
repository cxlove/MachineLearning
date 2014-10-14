from numpy import *
import matplotlib.pyplot as plt

def pca (dataSet , k = 10000000) :
	"""
	"""
	meanVal = mean (dataSet , 0)
	normalizedData = dataSet - meanVal
	covMatrix = cov (dataSet , rowvar = 0)
	eigenValue , eigenVector = linalg.eig (covMatrix)
	eigenIndex = argsort (eigenValue)
	chooseEigenIndex = eigenIndex[: -(k + 1) : -1]
	chooseEigenVector = eigenVector[: , chooseEigenIndex]
	lowDimData =  normalizedData * chooseEigenVector
	newDataSet = (lowDimData * chooseEigenVector.T) + meanVal
	return lowDimData , newDataSet

def showPca (origin , lowD , new) :
	"""
	"""
	plt.figure ('pca')
	plt.scatter (origin[: , 0].flatten ().A[0] , origin[: , 1].flatten().A[0] , marker = '^')
	plt.scatter (new[: , 0].flatten().A[0] , new[: , 1].flatten().A[0] , marker = 'o' , color = 'r')
	plt.show ()
