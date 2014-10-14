import PCA
from numpy import *

def loadData (fileAddress) :
	"""
	"""
	file = open (fileAddress).readlines ()
	data = []
	for line in file :
		data.append (map (float , line.strip().split()))
	return mat (data)

if __name__ == '__main__' :
	dataSet = loadData ('testSet.txt')
	lowDimData , newData = PCA.pca (dataSet , 1)
	PCA.showPca (dataSet , lowDimData , newData)
