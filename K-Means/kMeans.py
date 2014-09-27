#-*-coding:utf-8 -*-
from numpy import *
import time
import matplotlib.pyplot as plt

def dist (point1 , point2) : 
	"""
	The Euclidean distance of two point(vector)
	"""
	return sqrt (sum (power (point1 - point2 , 2)))  

def randomCentroids (dataSet , k) :
	"""
	choose k centroids with random
	"""
	cntPoint , dim = dataSet.shape
	used = [0 for i in range (cntPoint)]
	centroids = zeros ((k , dim))
	for i in range (k) :
		choose = random.randint (0 , cntPoint - 1)
		while used[choose] :
			choose = random.randint (0 , cntPoint - 1)
		used[choose] = 1
		centroids[i , :] = dataSet[choose , :]
	return centroids

def kmeans (dataSet , k) :
	"""
	The main process of k-means
	dataSet is a Matrix of data , k is the number of cluster
	"""
	cntPoint , dim = dataSet.shape
	centroids = randomCentroids (dataSet , k)  #the coordinate of centroids
	clusterChange = True
	#first column: which cluster belong to 
	#second column : the distance between the point and its centroid
	clusterAssign = mat (zeros ((cntPoint , 2)))  
	# until the cluster doesn't have any change
	while clusterChange : 
		clusterChange = False
		for i in range (cntPoint) :
			minDistance = 1e60
			minIndex = 0
			#for each cluster , calculate the distance , choose the centroid who is closest
			for j in range (k) :
				distacne = dist (centroids[j , :] , dataSet[i , :])
				if distacne < minDistance :
					minDistance , minIndex = distacne , j
			#update the cluster
			if clusterAssign[i , 0] != minIndex :
				clusterChange = True
				clusterAssign[i , : ] = minIndex , minDistance ** 2
		#for each cluster , calculate the new centroid
		for i in range (k) :
			pointInCluster = dataSet[nonzero (clusterAssign[: , 0].A == i)[0]]
			centroids[i , :] = mean (pointInCluster , axis = 0)

	return centroids , clusterAssign

def biKmeans (dataSet , k) :
	"""
	the main process of bisecting kmeans
	"""
	cntPoint , dim = dataSet.shape
	# all points belong to one cluster
	centroids = [mean (dataSet , axis = 0).tolist ()[0]]
	clusterAssign = mat (zeros ((cntPoint , 2)))
	for i in range (cntPoint) :
		clusterAssign[i , :] = 0 , dist (mat (centroids) , dataSet[i , :]) ** 2
	while len (centroids) < k :
		minimumSSE = 1e60
		# for each cluster , try to bisecting
		# then choose the best split
		for i in range (len (centroids)) :
			# get the point in cluster i
			pointInCluster = dataSet[nonzero (clusterAssign[: , 0].A == i)[0] , :]

			#use k-means to split the cluster 
			centroidsTemp , clusterAssignTemp = kmeans (pointInCluster , 2)
			sseNow = sum (clusterAssignTemp[: , 1])
			sseOther = sum (clusterAssign[nonzero (clusterAssign[: , 0].A != i)[0] , 1])
			# printCluster (pointInCluster , centroidsTemp , clusterAssignTemp , 2)

			if sseNow + sseOther < minimumSSE :
				minimumSSE = sseOther + sseNow
				bestIndex = i
				bestCentroids = centroidsTemp
				bestAssign = clusterAssignTemp.copy ()

		# update the cluster Index
		bestAssign[nonzero (bestAssign[: , 0].A == 1)[0] , 0] = len (centroids)
		bestAssign[nonzero (bestAssign[: , 0].A == 0)[0] , 0] = bestIndex

    	# according the new 2 sub-cluster , update the centroids
		centroids[bestIndex] = bestCentroids[0 , :]
		centroids.append (bestCentroids[1 , :])

		#update the distance and the index of clustere which the point belong to 
		clusterAssign[nonzero (clusterAssign[: , 0].A == bestIndex)[0] , :] = bestAssign

	return mat (centroids) , clusterAssign
				

def printCluster (dataSet , centroids , clusterAssign , k) :
	"""
	draw the k cluster and centroids in figure
	"""
	cntPoint , dim = dataSet.shape
	plt.figure (1)
	mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr'] 
	for i in range (cntPoint) :
		clusterIndex = int (clusterAssign[i , 0])
		plt.plot (dataSet[i , 0] , dataSet[i , 1] , mark[clusterIndex])

	mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
	for i in range (k):
		plt.plot (centroids[i , 0] , centroids[i , 1] , mark[i] , markersize = 12)

	plt.show ()