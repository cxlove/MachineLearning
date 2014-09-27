#-*-coding:utf-8-*-

from SVM import *
# load data
file = open ('data.txt')
dataSet = file.readlines ()
feature , labels = [] , []
for line in dataSet:
    lineArr = line.strip().split('\t')  
    feature.append([float(lineArr[0]), float(lineArr[1])])  
    labels.append(float(lineArr[2]))  
  
feature = mat(feature)  
labels = mat(labels).T  
train_x = feature[0:80, :]  
train_y = labels[0:80, :]  
test_x = feature[80:100, :]  
test_y = labels[80:100, :]  
# training
svm = trainSVM (train_x , train_y , 0.6 , 0.001 , 100 , ['rbf' , 1.0])

# print the SVM
showSVM (svm)

# testing
testSVM (svm , test_x , test_y)





