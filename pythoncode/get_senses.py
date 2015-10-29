import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

def Normalize (v):
    norm = np.sqrt(v.dot(v))
    if (norm == 0): 
       return v
    return v/norm

def GetContexts (fileName, dim):
	contextList = []
	with open(fileName,"r") as f:																#Read the context vectors from the file
		for line in f:
			numList = line.strip().split(' ')
			if (len(numList) < dim):
				continue
			wordVector = []
			for x in numList:
				wordVector.append(float(x))
			wordVector = Normalize(np.array(wordVector))
			contextList.append(wordVector)
	contextList = np.array(contextList)
	return contextList

def cluster(word, numClusters, dim): 									#Takes the word for which numClusters cluster need to be computed
	fileName = "wordcontexts" + str(dim) + "d/" + word + ".cont"
	contextList = GetContexts(fileName, dim)

	print "INPUT CONTEXTS COMPLETE"

	clf = KMeans(n_clusters=numClusters)
	result = clf.fit_predict(contextList)									#Finds cluster centres and assigns each vector a centre

	centroids = clf.cluster_centers_
	print centroids

	print result

		###############################################################################
	# Visualize the results on PCA-reduced contextList

	reduced_data = PCA(n_components=2).fit_transform(contextList)
	kmeans = KMeans(n_clusters=numClusters)
	kmeans.fit(reduced_data)

	# Step size of the mesh. Decrease to increase the quality of the VQ.
	h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

	# Plot the decision boundary. For that, we will assign a color to each

	#x_min, x_max = reduced_data[:, 0].min() + 1, reduced_data[:, 0].max() - 1
	#y_min, y_max = reduced_data[:, 1].min() + 1, reduced_data[:, 1].max() - 1
	x_min, x_max = reduced_data[:, 0].min(), reduced_data[:, 0].max()
	y_min, y_max = reduced_data[:, 1].min(), reduced_data[:, 1].max()
	

	print x_min, x_max
	print y_min, y_max
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

	print np.arange(x_min, x_max, h)
	print xx
	print yy
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
	plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
	          'Centroids are marked with white cross')
	plt.xlim(x_min, x_max)
	plt.ylim(y_min, y_max)
	plt.xticks(())
	plt.yticks(())
	plt.show()
