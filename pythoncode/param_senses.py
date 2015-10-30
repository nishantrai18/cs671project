from get_senses import *
from read_word import *

def PrecisionLimit (num):
	return "%.2f" % num

np.set_printoptions(precision=2)															#Pretty print
np.set_printoptions(suppress=True)

wordVec, wordID, numIDS, dim = GetWordVec("../huang50rep")

print "GETTING WORDVECS COMPLETE"

stopWords = GetWordFile("../stopwords", [])					#Takes two arguments, the second one is list of excluded words

print "GETTING STOPWORDS COMPLETE"														#Getting list of stopwords	

wordFreq = GetWordFile("../vocab.txt", stopWords)					#Getting words in order of word frequency

tfidf = {}
validWords = set(wordID)&set(wordFreq)								#Create set of valid words

multiList = []
trimNum = 1000																		#Get the number of words to consider
																					#Create the trimmed list of words
for i in range(0,trimNum):
	if (wordFreq[i] in validWords):
		multiList.append(wordFreq[i])

numClusters = input("INPUT NUMBER OF CLUSTERS : ")

fo = open("multisense/multisenses"+str(numClusters)+"n.vec","w")

for w in multiList:
	senses = cluster(w, numClusters, dim)
	fo.write(w + " " + str(len(senses)) + " " + str(dim) + "\n")
	for i in range(0,len(senses)):
		fo.write(str(i) + "\n")
		for num in senses[i]:
			fo.write(str(PrecisionLimit(num)+" ")
		fo.write("\n")

fo.close()