from numpy import *
import matplotlib.pyplot as plt
from Regression import *

def loadData (fileAddress) :
	"""
	"""
	file = open (fileAddress)
	input = file.readlines ()
	dataSet = []
	for line in input :
		data = map (float , line.split ())
		dataSet.append (data)

	dataSet.sort ()
	x , y = [] , []
	for line in dataSet :
		x.append (line[: -1])
		y.append (line[-1 :])
	return mat (x) , mat (y)

if __name__ == '__main__' :
	#normal linear regression
#	x , y = loadData ('ex0.txt')
#	w = standRegression (x , y)
#	predict = x * w
#	showRegression (x[: ,1] , y , predict)
	
	#lwlr 
#	x , y = loadData ('ex0.txt')
#	predict = lwlrTest (x , x , y , 0.01)
#	showRegression (x[: , 1] , y , predict)

	#Ridge Regression
#	x , y = loadData ('ex0.txt')
#	w = ridgeTest (x , y)
#	print w
	
	#forward stepwire regression
#	x , y = loadData ('ex0.txt')
#	w = stageWise (x , y)
#	print w


