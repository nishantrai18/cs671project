from get_senses import *
from read_word import *

import random

#from xmeans import *

np.set_printoptions(precision=2)															#Pretty print
np.set_printoptions(suppress=True)

"""
word = "hit"
dim = 50
fileName = "wordcontexts50d_1000(11-69)/" + word + ".cont"
data = GetContexts(fileName, dim)
print len(data)
PlotTSNE(data[:5000], [])
#ClusterPlot(data, 3)

"""
#cluster("hit",2,300)

#wordVec, wordID, numIDS, dim = GetWordVec("../googvecs")
wordVec, wordID, numIDS, dim = GetWordVec("../huang50rep")
stopWords = GetWordFile("../stopwords", [])					#Takes two arguments, the second one is list of excluded words
print "GETTING STOPWORDS COMPLETE"														#Getting list of stopwords	

wordFreq = GetWordFile("../vocab.txt", stopWords)					#Getting words in order of word frequency

wordDist = GetFreqFile("../wordfreq.txt")							#Get the frequencies of a word
maxSize = 5000000
noisyWords = GetNoisyList (wordDist, maxSize)

print noisyWords[:100]

print len(noisyWords)

wordList = wordFreq[400:450]

for word in wordList:
	fileName = "testing/" + word + ".winwords"
	contextList = GetContexts(fileName, dim)
	print "COMPUTING THE OPTIMAL K"
	k = OptimalCluster(word, contextList, dim, noisyWords, wordVec, wordID)
	print "THE BEST K IS",k

"""
tfidf = {}
validWords = set(wordID)&set(wordFreq)								#Create set of valid words

multiList = []
trimNum = 2500																		#Get the number of words to consider
																					#Create the trimmed list of words
for i in range(0,trimNum):
	if (wordFreq[i] in validWords):
		multiList.append(wordFreq[i])

data = []

for w in multiList:
	data.append(wordVec[wordID[w]])

PlotTSNE(data, multiList)
"""

"""
import matplotlib.pyplot as plt

x = np.array([np.random.normal(loc, 0.1, 20) for loc in np.repeat([1,2], 2)]).flatten()
y = np.array([np.random.normal(loc, 0.1, 20) for loc in np.tile([1,2], 2)]).flatten()

x_means = XMeans(random_state = 1).fit(np.c_[x,y]) 
print(x_means.labels_)
print(x_means.cluster_centers_)
print(x_means.cluster_log_likelihoods_)
print(x_means.cluster_sizes_)

plt.rcParams["font.family"] = "Hiragino Kaku Gothic Pro"
plt.scatter(x, y, c = x_means.labels_, s = 30)
plt.scatter(x_means.cluster_centers_[:,0], x_means.cluster_centers_[:,1], c = "r", marker = "+", s = 100)
plt.xlim(0, 3)
plt.ylim(0, 3)
plt.title("x-means(2000)")
plt.show()
"""