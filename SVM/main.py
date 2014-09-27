#-*-coding:utf-8-*-

from SVM import *
# load data
file = open ('data.txt')
dataSet = file.readlines ()
feature , label = [] , []
for line in dataSet :
	data = map (double , line.split ())
	feature.append (data[ : -1])
	label.append (data[-1 :])

feature = mat (feature)
label = mat (label)

train_x = feature[0 : 80]
train_y = label[0 : 80]
test_x = feature[80 :]
test_y = label[80 :]

# training
svm = trainSVM (train_x , train_y , 0.6 , 0.001 , 50 , ['linear'])

# print the SVM
showSVM (svm)

# testing
testSVM (svm , test_x , test_y)





