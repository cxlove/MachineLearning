from Apriori import *

if __name__ == '__main__' :
	dataSet = loadDataSet ()
	L , supportData = Apriori (dataSet , 0.5)
	print L
	generateRule (L , supportData , 0.5)
