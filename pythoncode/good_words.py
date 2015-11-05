import numpy as np
import math

from read_word import *
from get_senses import *
from create_contexts import *

wordVec = {}																		#Takes integer as argument and maps it to a word vector
wordID = {}																			#Takes a word and maps it to an id 
numIDS = {}																			#Inverse mapping for wordVec
dim = 0

#wordVec, wordID, numIDS, dim = GetWordVec("../googvecs")
wordVec, wordID, numIDS, dim = GetWordVec("../huang50rep")
#wordVec, wordID, numIDS, dim = GetWordVec("../neel50d6K")
print "INPUT WORD VECTORS COMPLETE"

stopWords = GetWordFile("../stopwords", [])					#Takes two arguments, the second one is list of excluded words
print "GETTING STOPWORDS COMPLETE"														#Getting list of stopwords	

wordFreq = GetWordFile("../vocab.txt", stopWords)					#Getting words in order of word frequency

wordDist = GetFreqFile("../wordfreq.txt")							#Get the frequencies of a word
maxSize = 5000000
noisyWords = GetNoisyList (wordDist, maxSize)

tfidf = {}
validWords = set(wordID)&set(wordFreq)								#Create set of valid words

cnt = 0
with open("../tfidf.txt","r") as f:																#Get the tfidf of words
	for line in f:
		tfid = line.strip().split()[0]
		if (cnt >= len(wordFreq)):
			break
		tfidf[wordFreq[cnt]] = float(tfid)
		cnt += 1

raw_input("ARE YOU SURE YOU WANT TO CONSTRUCT CONTEXT VECTORS (Y/N) : ")

print "GETTING TFIDF COMPLETE"														#Getting list of stopwords	
print wordFreq[:100]
#print wordVec.keys()[:100] 	

multiList = []

trimNum = 6000																		#Get the number of words to consider

for i in range(0,trimNum):															#Create the trimmed list of words
	if (wordFreq[i] in validWords):
		multiList.append(wordFreq[i])

sz = len(multiList)
print len(multiList)
print "SIZE IS ", sz

###############TFIDF PRUNING########################
tfidfList = tfidf.values()
tfidfList.sort()
#tmp = tfidfList[int(-(0.99)*len(tfidfList))]											#Change this hyper parameter to get different results
tmp = 2
print "THE PRUNED TFIDF IS",tmp
for x in tfidf.keys():
	if (tfidf[x] < tmp):
		tfidf[x] = 0
#################PRUNING COMPLETE####################

np.set_printoptions(precision=3)															#Pretty print
np.set_printoptions(suppress=True)

#Find the good words

#First open the files of a couple of words
#We first read the files piece wise (Since they are broken into multiple pieces)
#We go over the file and compute the corresponding context vector for it
#We append the context vector for a word in a file named <word>.winwords
#We compute the vectors of only the words which have their files open

i = 0																		#Starting point

window = 5

while (i < trimNum):
	wordSlice = multiList[i:i+1000]
	selWords = []

	for w in wordSlice:
		if (w.isalpha()):
			selWords.append(w)

	i += 1000

	fileList = {}
	for j in selWords:
		fileList[j] = open("goodwords"+str(dim)+"d_huangB/"+j+".winwords", "a")

		#wordcontexts_A : It contains naive construction of context vectors.
		#wordcontexts_B : It involves the usage of similarity metric while computing the context vectors.
		#wordcontexts_large : It contains files from 11-150, otherwise its 11-39

	for m in range(11,25):
		fileName = "../testfiles_sm/tf00"+str(m)
		print fileName,
		MakeContextVecWithGoodWords(fileName, wordVec, dim, wordID, validWords, tfidf, stopWords, selWords, window, fileList)
	
		print m, "IS DONE",
		if(m%3==0):
			print "\n",

	for j in selWords:
		fileList[j].close()
	
	print i, "IS DONE"