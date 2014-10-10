from numpy import *
import matplotlib.pyplot as plt

def normalized (x) :
	"""
	"""
	xMean = mean (x , 0)
	ans = mat (ones ((shape (x)[0] , shape (x)[1])))
	ans[: , 1] = (x[: , 1] - xMean[: , 1]) / var (x[: , 1] , 0)
	return x

def rssError (a , b) :
	return (array (a - b) ** 2).sum ()

def standRegression (x , y) :
	"""
	standard liner regression
	w = (X^T*X)^-1*X^T*Y
	"""
	n , m = x.shape 
	xtx = x.T * x
	if linalg.det (xtx) == 0.0 :
		print 'No inverse'
		return 
	return xtx.I * x.T * y

def lwlr (testX , x , y , k = 1.0) :
	"""
	Locally Weighted Linear Regression
	gauss kernel
	w = (x^T*w*x)^-1*x^T*w*y
	w(i) = exp (\frac{|x^i - x|}{-2*k^2})
	"""
	n , m = x.shape 
	weight = mat (eye (n))
	for i in range (n) :
		diff = x[i , :] - testX
		weight[i , i] = exp (diff * diff.T / (-2.0 * k ** 2))
	xtx = x.T * weight * x
	if linalg.det (xtx) == 0.0 :
		print 'NO inverse'
		return 
	w = xtx.I * x.T * weight * y
	return testX * w

def lwlrTest (testX , x , y , k = 1.0) :
	"""
	"""
	n , m = testX.shape
	predict = zeros (n)
	for i in range (n) :
		predict[i] = lwlr (testX[i] , x , y , k)
	return predict

def ridgeRegression (x , y , lab = 0.5) :
	"""
	ridge regression
	w = (x^T*x+lamada * I)^-1*x^T*y
	"""
	n , m = x.shape
	xtx = x.T * x + lab * mat (eye (m))
	if linalg.det (xtx) == 0.0 :
		print 'No inverse'
		return 
	return xtx.I * x.T * y

def ridgeTest (x , y) :
	"""
	"""
	n , m = x.shape
	x = normalized (x)

	numTest = 30
	wMat = mat (zeros ((numTest , m)))
	for i in range (numTest) :
		w = ridgeRegression (x , y , exp (i - 10))
		wMat[i , :] = w.T
	return wMat

def stageWise (x , y , step = 0.01 , numIter = 100) :
	"""
	"""
	n , m = x.shape
	x = normalized (x)
	w = standRegression (x , y)
	for i in range (numIter) :
		error = 1e60	
		for j in range (m) :
			for k in [-1 , 1] :
				wt = w.copy ()
				wt[j , 0] += k * step
				predict = x * wt
				rssE = rssError (predict , y)
				if rssE < error :
					error = rssE
					wBest = wt.copy ()
		w = wBest.copy ()
	return w

def showRegression (x , y , predict) :
	"""
	"""
	plt.figure ('regression')
	plt.plot (x.flatten() , y.flatten() , 'ro')
	plt.plot (x , predict)
	plt.show ()

