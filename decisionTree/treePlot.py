#-*-coding:utf-8-*-
import matplotlib.pyplot as plt

decisionNode = dict (boxstyle = 'sawtooth' , fc = '0.8')
leafNode = dict (boxstyle = 'round4' , fc = '0.8')
arrow_args = dict (arrowstyle = '<-')

def calTreeLeaf (tree) :
	"""
	calculate the number of leaf in tree
	"""
	numLeaf = 0
	firstVec = tree.keys()[0]
	secondVec = tree[firstVec]
	for key in secondVec.keys () :
		if type(secondVec[key]).__name__ == 'dict' :
			numLeaf += calTreeLeaf (secondVec[key])
		else : numLeaf += 1
	return numLeaf

def calTreeDepth (tree) :
	"""
	calculate the maximum depth of the tree
	"""
	maxDepth = 0
	firstVec = tree.keys()[0]
	secondVec = tree[firstVec]
	for key in secondVec.keys () :
		curDepth = 1
		if type(secondVec[key]).__name__ == 'dict' :
			curDepth = 1 + calTreeDepth (secondVec[key])
		if curDepth > maxDepth :
			maxDepth = curDepth
	return maxDepth

def plotNode (nodeText , curPoint , prePoint , nodeType) :
	"""
	from prePoint to curPoint draw a arrow
	nodeText in curPoint
	"""
	createPlot.ax1.annotate (nodeText , xy = prePoint , xycoords = 'axes fraction' , \
	 xytext = curPoint , textcoords = 'axes fraction' , va = 'center' , ha = 'center' ,\
	  bbox = nodeType , arrowprops = arrow_args)

def plotText (curPoint , prePoint , textString) :
	"""
	print the textString in figure between the curPoint and prePoint
	"""
	xMid = (curPoint[0] + prePoint[0]) / 2.0
	yMid = (curPoint[1] + prePoint[1]) / 2.0
	createPlot.ax1.text (xMid , yMid , textString , fontsize = 10 , rotation = 45)

def plotTree (tree , prePoint , textString) :
	"""
	draw the tree below prePoint
	textString is in the arrow from prePoint to root 
	"""
	numLeaf = calTreeLeaf (tree)
	numDepth = calTreeDepth (tree)
	firstVec = tree.keys()[0]
	secondVec = tree[firstVec]
	curPoint = (plotTree.axisX + (1.0 + numLeaf) / 2.0 / plotTree.totalWidth , plotTree.axisY)
	plotNode (firstVec , curPoint , prePoint , decisionNode)
	plotText (curPoint , prePoint , textString)
	plotTree.axisY -= 1.0 / plotTree.totalHeight
	for key in secondVec.keys () :
		if type(secondVec[key]).__name__ == 'dict' :
			plotTree (secondVec[key] , curPoint , str (key))
		# leaf
		else :
			plotTree.axisX += 1.0 / plotTree.totalWidth
			plotNode (secondVec[key] , (plotTree.axisX , plotTree.axisY) , curPoint , leafNode)
			plotText ((plotTree.axisX , plotTree.axisY) , curPoint , str (key))
	plotTree.axisY += 1.0 / plotTree.totalHeight

def createPlot (tree) :
	"""
	create the plot of the decision tree
	"""
	plotTree.totalWidth = float (calTreeLeaf(tree))
	plotTree.totalHeight = float (calTreeDepth (tree))
	plotTree.axisX = -0.5 / plotTree.totalWidth
	plotTree.axisY = 1.0
	createPlot.ax1 = plt.subplot (111 , frameon = False)
	plotTree (tree , (0.5 , 1.0) , '')
	plt.show ()