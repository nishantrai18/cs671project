from get_senses import *
from read_word import *
from create_contexts import *

np.set_printoptions(precision=2)															#Pretty print
np.set_printoptions(suppress=True)

#wordVec, wordID, numIDS, dim = GetWordVec("../huang50rep")
#wordVec, wordID, numIDS, dim = GetWordVec("../googvecs")
wordVec, wordID, numIDS, dim = GetWordVec("../neel50d6K")

print "GETTING WORDVECS COMPLETE"

stopWords = GetWordFile("../stopwords", [])					#Takes two arguments, the second one is list of excluded words

print "GETTING STOPWORDS COMPLETE"														#Getting list of stopwords	

wordFreq = GetWordFile("../vocab.txt", stopWords)					#Getting words in order of word frequency

wordDist = GetFreqFile("../wordfreq.txt")							#Get the frequencies of a word
maxSize = 5000000
noisyWords = GetNoisyList (wordDist, maxSize)

optKWord = {}

"""
###################Use this in case we have already computed optimal clusters#############
multiWordVec, multiWordID, multiNumIDS, dim = GetMultiWordVec("multisense/npmultisenses50d_huangB.vec")	

for w in multiWordID.keys():
	optKWord[w] = len(multiWordVec[multiWordID[w]])

print "INPUT WORD VECTORS/ MULTISENSE VECTORS AND OPTK COMPUTATION COMPLETE"
##########################################################################################
"""

tfidf = {}
validWords = set(wordID)&set(wordFreq)								#Create set of valid words

multiList = []
trimNum = 6000																		#Get the number of words to consider
																					#Create the trimmed list of words
for i in range(0,trimNum):
	if (wordFreq[i] in validWords):
		multiList.append(wordFreq[i])

fo = open("multisense/npmultisenses"+str(dim)+"d_neellargeB.vec","w")

cnt=0

for w in multiList:
	if (not w.isalpha()):
		continue

	if(cnt%5==0):
		print "\n",
	print cnt, 
	cnt+=1

	senses = NonParCluster(w, dim, noisyWords, wordVec, wordID, optKWord)
	fo.write(w + " " + str(len(senses)) + " " + str(dim) + "\n")
	for i in range(0,len(senses)):
		fo.write(str(i) + "\n")
		for num in senses[i]:
			fo.write(str(PrecisionLimit(num)+" "))
		fo.write("\n")

fo.close()