from logisticRegression import *

def loadData (fileAddress) :
	file = open (fileAddress)
	dataSet = file.readlines ()
	data_x = []
	data_y = []
	for data in dataSet :
		vecData = data.split ()
		if vecData[-1] == '?' : continue
		for i in range (len (vecData)) :
			if vecData[i] == '?' : vecData[i] = 0.0
			else : vecData[i] = float (vecData[i])
		del (vecData[2])
		vecData.insert (0 , 1)
		data_y.append (vecData[-1 : ])
		data_x.append (vecData[ : 21])
	return mat (data_x) , mat (data_y)


if __name__ == '__main__' :
	print 'setp 1 : load dataset'
	train_x , train_y = loadData (r'horse-colic.data')
	test_x , test_y = loadData (r'horse-colic.test')
	print 'step 2 : training'
	weight = showLogistic (train_x , train_y)
	print 'step 3 : testing'
	print 'step 4 : the accuracy is %f!' % (testLogistic (test_x , test_y , weight) * 100)


