from get_senses import *
from read_word import *

import random
import sys

#from xmeans import *

np.set_printoptions(precision=2)															#Pretty print
np.set_printoptions(suppress=True)

def ExtractRoot (word):
	tmp = word.split('_')
	return tmp[0]

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

#wordVec, wordID, numIDS, dim = GetWordVec("../googvecs")
wordVec, wordID, numIDS, dim = GetWordVec("../huang_vectors_skip.txt")

stopWords = GetWordFile("../stopwords", [])					#Takes two arguments, the second one is list of excluded words
print "GETTING STOPWORDS COMPLETE"														#Getting list of stopwords	

wordFreq = GetWordFile("../vocab.txt", stopWords)					#Getting words in order of word frequency
print "GETTING VOCAB COMPLETE"

multiList = []
trimNum = 3000																		#Get the number of words to consider
																					#Create the trimmed list of words

#print wordFreq[:trimNum]

wordList = wordID.keys()
wordList.sort()

wordList = wordList[100000:]

print len(wordList)

print "SORTING DONE"
sys.stdout.flush()

i = 0
j = 0 
while (i < len(wordList)) and (j < trimNum):
	root = ExtractRoot(wordList[i])
	if ((root in wordID) and (root in wordFreq) and (root.isalpha())):
		multiList.append(wordList[i])
		print wordList[i],
		j += 1
	i += 1		

data = []

for w in multiList:
	data.append(wordVec[wordID[w]])

print len(data)

print multiList

PlotTSNE(data, multiList)