from logisticRegression import *

def loadData (fileAddress) :
	file = open (fileAddress)
	dataSet = file.readlines ()
	data_x = []
	data_y = []
	for data in dataSet :
		vecData = map (float , data.split ())
		vecData.insert (0 , 1)
		data_x.append (vecData[ : -1])
		data_y.append (vecData[-1 : ])
	return mat (data_x) , mat (data_y)


if __name__ == '__main__' :
	print 'setp 1 : load dataset'
	train_x , train_y = loadData (r'data.txt')
	print 'step 2 : training'
	weight = showLogistic (train_x , train_y)
	print 'step 3 : testing'
	print 'step 4 : the accuracy is %f!' % (testLogistic (train_x , train_y , weight) * 100)


