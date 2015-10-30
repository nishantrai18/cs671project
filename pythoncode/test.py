from get_senses import *
from read_word import *

np.set_printoptions(precision=2)															#Pretty print
np.set_printoptions(suppress=True)

#cluster("hit",2,300)

wordVec, wordID, numIDS, dim = GetWordVec("../huang50rep")

stopWords = GetWordFile("../stopwords", [])					#Takes two arguments, the second one is list of excluded words

print "GETTING STOPWORDS COMPLETE"														#Getting list of stopwords	

wordFreq = GetWordFile("../vocab.txt", stopWords)					#Getting words in order of word frequency

tfidf = {}
validWords = set(wordID)&set(wordFreq)								#Create set of valid words


multiList = []
trimNum = 1500																		#Get the number of words to consider
																					#Create the trimmed list of words
for i in range(0,trimNum):
	if (wordFreq[i] in validWords):
		multiList.append(wordFreq[i])

data = []

for w in multiList:
	data.append(wordVec[wordID[w]])

PlotTSNE(data, multiList)