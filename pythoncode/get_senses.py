import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.cluster import MeanShift, estimate_bandwidth

from create_contexts import *

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

	print word, len(contextList), numClusters, "::",
	
	if(len(contextList) < numClusters):
		return []

	clf = KMeans(n_clusters=numClusters, n_init=10, max_iter=75)				#In case of normalised data points, euclidean k means is the same as spherical
	result = clf.fit_predict(contextList)										#Finds cluster centres and assigns each vector a centre

	centroids = clf.cluster_centers_

	return centroids

def NonParCluster(word, dim, noisyWords, wordVec, wordID, optKWord): 									#Computes a clustering after estimating the number of clusters
																										#optKWord contains the pre known optimal value
	fileName = "goodwords50d_huangB/" + word + ".winwords"
	contextList = GetContexts(fileName, dim)

	#print len(contextList),":",

	optK = 0
	if word not in optKWord:
		optK = OptimalCluster(word, contextList, dim, noisyWords, wordVec, wordID)
		print "I DID THIS COMPUTATION"
	else:
		optK = optKWord[word]
	print optK,

	if (optK <= 1):
		return []
	return cluster(word, optK, dim)

def GetValidationContexts (fileName, dim):
	validationList = []
	goodWords = []
	with open(fileName,"r") as f:																#Read the context vectors from the file
		for line in f:
			numList = line.strip().split(' ')
			if (len(numList) < dim):
				if (numList[0].isdigit()):														#Check if it is a valid line
					numWords = int(numList[0])
					goodWords = numList[1:]
					goodWords = set(goodWords)	
			elif (len(numList) == dim):															
				wordVector = []
				for x in numList:
					wordVector.append(float(x))	
				wordVector, status = Normalize(np.array(wordVector))							#First read the word vector
				if (status == 0):
					continue
				validationList.append((goodWords, wordVector))
	return validationList

#Presently finding the optimal on a reduced subset of contexts
#Change whether we use validation list or context list for estimation

def OptimalCluster(word, contextList, dim, noisyWords, wordVec, wordID): 						#Takes the word for which optimal clusters need to be computed
																								#Does it on the basis of a function to be optimised
	fileName = "goodwords50d_huangB/"+word+".winwords"
	candK = []
	for x in range(1,20):
		candK.append(x)

	maxEstimate = -1000000000
	optK = 0
	validationList = GetValidationContexts(fileName, dim)

	for numClusters in candK:
		if (len(contextList) < numClusters):
			continue
		clf = KMeans(n_clusters=numClusters, n_init=5, max_iter=35)					#In case of normalised data points, euclidean k means is the same as spherical
		result = clf.fit_predict(contextList)										#Finds cluster centres and assigns each vector a centre
		centroids = clf.cluster_centers_
		estimate = GetEstimate (word, centroids, validationList, dim, noisyWords, wordVec, wordID)
		print "%.4f" % estimate,

		change = ((estimate - maxEstimate)/abs(maxEstimate))
		print "%.4f" % change,
		if (change < (0.005)):																			#Change the hyperparameter here
			break

		maxEstimate = estimate
		optK = numClusters

	return optK


#Read random words from a file (Same for all words) and store in dictionary. Format is
#<word> <count>
#This dictionary will be global
#### WHY NOT CONSTRUCT THE FILE PURELY ON THE BASIS OF THE DISTRIBUTION###############

#Read good words from file containing data in format
#<numgwords> <gw1> <gw2> ..... <gwn>
#<wordvector line containing dim lines>
#Assign cluster to each word vector
#Keep list of cluster dictionaries with counts of good words
#Finally compute score (softmax) to get a value. 
#For negative sampling, divide the original corpus into k equal parts
#Also try doing actually negative sampled things. (Depending on the time taken)

def GetEstimate (word, clusters, validationList, dim, noisyWords, wordVec, wordID):	#Takes the target word, clusters represent lists numClusters cluster centers
																					#ValidationList is a list of the contexts and good words
																					#noisyWords is a dictionary containing count of the noisy words.
																					#Wordvec is used to get the word vector during estimation
	numClusters = len(clusters)
	goodWordCount = [dict() for x in range(numClusters)]
	noisyWordCount = [dict() for x in range(numClusters)]
	
	negativeSampleSize = 2
	numWords = 0
	goodWords = []
	cnt = 0

	for i in validationList:
		wordVector = i[1]
		goodWords = i[0]
		clusterID = AssignCluster(wordVector, clusters)									#Get the actual cluster of the word
		for x in goodWords:																#Increment the good word count
			if (x not in goodWordCount[clusterID]):
				goodWordCount[clusterID][x] = 1 										
			else:
				goodWordCount[clusterID][x] += 1
		status = 0
		while (status < (len(goodWords)*negativeSampleSize)):							#Negative sampling of the word
			if (noisyWords[cnt] not in goodWords):
				if (noisyWords[cnt] not in noisyWordCount[clusterID]):
					noisyWordCount[clusterID][noisyWords[cnt]] = 1
				else:
					noisyWordCount[clusterID][noisyWords[cnt]] += 1
				status += 1
			cnt = (cnt + 1)%len(noisyWords)

	expGood = 0																					#Computation of the cost function
	expNoisy = 0
	for i in range(0,len(clusters)):
		for k in goodWordCount[i].keys():
			expGood += np.log(sigmoid(clusters[i].dot(wordVec[wordID[k]])))*goodWordCount[i][k]
	for i in range(0,len(clusters)):
		for k in noisyWordCount[i].keys():
			expNoisy += np.log(sigmoid(-clusters[i].dot(wordVec[wordID[k]])))*noisyWordCount[i][k]

	return expNoisy + expGood


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