import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.cluster import MeanShift, estimate_bandwidth

def Normalize (v):
    norm = np.sqrt(v.dot(v))
    if (norm == 0): 
       return v, 0
    return (v/norm), 1

def GetContexts (fileName, dim):
	contextList = []
	with open(fileName,"r") as f:																#Read the context vectors from the file
		for line in f:
			numList = line.strip().split(' ')
			if (len(numList) != dim):
				continue
			wordVector = []
			for x in numList:
				wordVector.append(float(x))
			wordVector, status = Normalize(np.array(wordVector))
			if (status == 1):
				contextList.append(wordVector)
	contextList = np.array(contextList)
	return contextList

def cluster(word, numClusters, dim): 									#Takes the word for which numClusters cluster need to be computed
	fileName = ""
	if (dim == 50):
		fileName = "wordcontexts50d_huanglargeB/" + word + ".cont"
	else:
		fileName = "wordcontexts300d_6000(11-39)/" + word + ".cont"
	
	contextList = GetContexts(fileName, dim)

	print word, len(contextList),
	
	if(len(contextList) < numClusters):
		return []

	clf = KMeans(n_clusters=numClusters, n_init=10, max_iter=75)				#In case of normalised data points, euclidean k means is the same as spherical
	result = clf.fit_predict(contextList)										#Finds cluster centres and assigns each vector a centre

	centroids = clf.cluster_centers_

	return centroids

def ClusterPlot (data, numClusters):
	###############################################################################
	# Visualize the results on PCA-reduced contextList

	reduced_data = PCA(n_components=2).fit_transform(data)

	print "DATA REDUCED"

	kmeans = KMeans(n_clusters=numClusters)
	kmeans.fit(reduced_data)

	# Plot the decision boundary. For that, we will assign a color to each
	x_min, x_max = reduced_data[:, 0].min(), reduced_data[:, 0].max()
	y_min, y_max = reduced_data[:, 1].min(), reduced_data[:, 1].max()
	
	# Step size of the mesh. Decrease to increase the quality of the VQ.
	h = ((x_max-x_min)/100)     # point in the mesh [x_min, m_max]x[y_min, y_max].

	print x_min, x_max
	print y_min, y_max
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

	# Obtain labels for each point in mesh. Use last trained model.
	Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

	# Put the result into a color plot
	Z = Z.reshape(xx.shape)
	plt.figure(1)
	plt.clf()
	plt.imshow(Z, interpolation='nearest',
	           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
	           cmap=plt.cm.Paired,
	           aspect='auto', origin='lower')

	plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
	# Plot the centroids as a white X
	centroids = kmeans.cluster_centers_
	plt.scatter(centroids[:, 0], centroids[:, 1],
	            marker='x', s=169, linewidths=3,
	            color='w', zorder=10)

	#Adds labels to the plots
	"""labels = ['point{0}'.format(i) for i in range(len(reduced_data))]
	for label, x, y in zip(labels, reduced_data[:, 0], reduced_data[:, 1]):
	    plt.annotate(
	        label, 
	        xy = (x, y), xytext = (-20, 20),
	        textcoords = 'offset points', ha = 'right', va = 'bottom',
	        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
	        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
	"""

	plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
	          'Centroids are marked with white cross')
	plt.xlim(x_min, x_max)
	plt.ylim(y_min, y_max)
	plt.xticks(())
	plt.yticks(())
	plt.show()


def PlotTSNE (data, labels):										#Takes the data and the labels
	# Visualize the results on TSNE reduced data

	print "BUSY IN TSNE"

	model = TSNE(n_components=2, random_state=0)
	reduced_data = model.fit_transform(data)

	print "DATA REDUCED"

	# Plot the decision boundary. For that, we will assign a color to each
	x_min, x_max = reduced_data[:, 0].min(), reduced_data[:, 0].max()
	y_min, y_max = reduced_data[:, 1].min(), reduced_data[:, 1].max()
	
	plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
	
	#Adds labels to the plot
	for label, x, y in zip(labels, reduced_data[:, 0], reduced_data[:, 1]):
	    plt.annotate(
	        label, 
	        xy = (x, y), xytext = (-20, 20),
	        textcoords = 'offset points', ha = 'right', va = 'bottom',
	        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
	        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
	

	plt.title('TSNE Plot')
	plt.xlim(x_min, x_max)
	plt.ylim(y_min, y_max)
	plt.xticks(())
	plt.yticks(())
	plt.show()