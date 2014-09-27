from decisionTree import *
from treePlot import *
import pickle
from classifyDecisionTree import *

def storeTree (input , filename) :
	"""
	use the module of pickle to store the tree
	"""
	cout = open (filename , 'w')
	pickle.dump (input , cout)
	cout.close ()

def grabTree (filename) :
	"""
	load the tree
	"""
	cin = open (filename , 'r')
	return pickle.load (cin)

if __name__ == '__main__' :
	fileAddress = 'E:/Python/decisionTree/tree.txt'
	storeTree (mainProcess () , fileAddress)
	decisionTree = grabTree (fileAddress)
	createPlot (decisionTree)

	# print classify (decisionTree , ['no surfacing' , 'flippers'] , [1 , 0])
	# print classify (decisionTree , ['no surfacing' , 'flippers'] , [1 , 1])

	