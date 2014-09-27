#-*-coding:utf-8-*-

from SVM import *
# load data
file = open ('training.txt')
dataSet = file.readlines ()
train_x , train_y = [] , []
for line in dataSet :
	data = line.split ()
	train_y.append ([float (data[0])])
	x = [0] * 123
	for i in range (1 , len (data)) :
		a = data[i].split (':')
		x[int (a[0]) - 1] = 1.0
	train_x.append (x)

file = open ('testing.txt')
dataSet = file.readlines ()
test_x , test_y = [] , []
for line in dataSet :
	data = line.split ()
	test_y.append ([float (data[0])])
	x = [0] * 123
	for i in range (1 , len (data)) :
		a = data[i].split (':')
		x[int (a[0]) - 1] = 1.0
	test_x.append (x)

train_x = mat (train_x)
train_y = mat (train_y)
test_x = mat (test_x)
test_y = mat (test_y)

# training
svm = trainSVM (train_x , train_y , 0.6 , 0.001 , 100 , ['rbf' , 1.0])

# print the SVM
# showSVM (svm)

# testing
testSVM (svm , test_x , test_y)





