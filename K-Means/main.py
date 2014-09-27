#-*-coding:utf-8 -*-
from numpy import *
import time
import matplotlib.pyplot as plt
from kMeans import *

def loadData () :
	dataSet = []
	file = open (r'E:/Python/data.in')
	for line in file.readlines () :
		a = line.strip().split ()
		dataSet.append ((float (a[0]) , float (a[1])))

	dataSet = mat (dataSet)
	centroids , clusterAssign = biKmeans (dataSet , 4)

	printCluster (dataSet , centroids , clusterAssign , 4)

if __name__ == '__main__' :
	loadData ()
