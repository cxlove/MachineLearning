from fpGrowth import *

def loadSimData () :
	"""
	"""
	return [['r' , 'z' , 'h' , 'j' , 'p'] ,
			['z' , 'y' , 'x' , 'w' , 'v' , 'u' , 't' , 's'] ,
			['z'] ,
			['r' , 'x' , 'n' , 'o' , 's'] ,
			['y' , 'r' , 'x' , 'z' , 'q' , 't' , 'p'] ,
			['y' , 'z' , 'x' , 'e' , 'q' , 's' , 't' , 'm']]

if __name__ == '__main__' :
#	dataSet = loadSimData () 
	dataSet = [line.split () for line in open ('kosarak.dat').readlines ()]
	dataSet = creatInitData (dataSet)
	minSupport = 100000
	tree , header = creatFpTree (dataSet , minSupport)
	tree.display ()
	freq = []
	fpGrowth (tree , header , minSupport , set([]) , freq)
	print freq
