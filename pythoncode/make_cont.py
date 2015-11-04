import numpy as np
import math

from read_word import *
from get_senses import *

def PrecisionLimit (num):
	return "%.3f" % num

def CleanWord (word):
	symbols = [',','\"',"\'",".","?","/","(",")"]
	for c in symbols:
		word = word.replace(c,'')
	return word.lower()

def sigmoid(x):
	return 1 / (1 + math.exp(-x))

def sim (wA, wB, wordVec, wordID):									#Gives the cosine similarity
	vecA = wordVec[wordID[wA]]
	vecB = wordVec[wordID[wB]]
	dot = vecA.dot(vecB)
	normA = np.sqrt(vecA.dot(vecA))
	normB = np.sqrt(vecB.dot(vecB))
	similarity = (dot/(normA*normB))
	return sigmoid(similarity)

def MakeContextVec (fileName, wordVec, dim, wordID,  											
					validWords, tfidf, stopWords, simWords,										
					selWords, window, fileList):												#tfidf's, words to be considered as input
																								#simWords is a dictionary with similarities
																								#window is the length considered to the left and right
																								#vocabID is the vocabulary integer mapping 
	with open(fileName,"r") as f:																#Read the word vectors from the file
		for line in f:
			sentence = line.strip().split(' ')													#Get a list of words
			for i in range(0, len(sentence)):
				sentence[i] = CleanWord(sentence[i])

			for i in range (0, len(sentence)):
				if (sentence[i] in selWords):													#If current word is in the context list
					wordVector = np.zeros(dim)								
					for j in range(i-window, i+window):
						if (j < 0):
							j = -1
						elif (j >= len(sentence)):
							break
						elif (j == i):
							continue
						elif (sentence[j] in validWords):											#Checks if present in vocabulary
							if(sentence[j] not in stopWords):
								if (tfidf[sentence[j]] > 0):
									#print (tfidf[sentence[j]])
									#print (wordVec[wordID[sentence[j]]])
									wordVector = wordVector + \
									(tfidf[sentence[j]]*sim(sentence[i], sentence[j], wordVec, wordID))*wordVec[wordID[sentence[j]]]					
																							#Change here to alter the construction of context vectors
					if (wordVector.dot(wordVector) > 0):
						wordVector, status = Normalize(wordVector)
						if (status == 0):
							continue
						for k in range(0,len(wordVector)):
							fileList[sentence[i]].write(str(PrecisionLimit(wordVector[k]))+" ")
						fileList[sentence[i]].write("\n")

wordVec = {}																		#Takes integer as argument and maps it to a word vector
wordID = {}																			#Takes a word and maps it to an id 
numIDS = {}																			#Inverse mapping for wordVec
dim = 0

#wordVec, wordID, numIDS, dim = GetWordVec("../googvecs")
#wordVec, wordID, numIDS, dim = GetWordVec("../huang50rep")
wordVec, wordID, numIDS, dim = GetWordVec("../neel50d6K")

print "INPUT WORD VECTORS COMPLETE"

stopWords = GetWordFile("../stopwords", [])					#Takes two arguments, the second one is list of excluded words

print "GETTING STOPWORDS COMPLETE"														#Getting list of stopwords	

wordFreq = GetWordFile("../vocab.txt", stopWords)					#Getting words in order of word frequency

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

print "GETTING TFIDF COMPLETE"														#Getting list of stopwords	

print wordFreq[:100]
#print wordVec.keys()[:100] 	

multiList = []
vocabID = {}
invVocab = {}
numIDS = 0

trimNum = 6000																		#Get the number of words to consider
																					#Create the trimmed list of words
for i in range(0,trimNum):
	if (wordFreq[i] in validWords):
		multiList.append(wordFreq[i])

sz = len(multiList)

print len(multiList)

print "SIZE IS ", sz

simWords = {}

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

"""
################CREATE SIMILARITY DICTIONARY################

for w in multiList:
	for x in tfidf.keys():
		if (tfidf.get(x, 0) > 0):
			simWords[(w,x)] = sim(w, x, wordVec, wordID)
			simWords[(x,w)] = simWords[(w,x)]
############################################################
"""

np.set_printoptions(precision=3)															#Pretty print
np.set_printoptions(suppress=True)

#Construct the context vectors

#First open the files of a couple of words
#We first read the files piece wise (Since they are broken into multiple pieces)
#We go over the file and compute the corresponding context vector for it
#We append the context vector for a word in a file named <word>.cont
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
		fileList[j] = open("wordcontexts"+str(dim)+"d_neelB/"+j+".cont", "a")

		#wordcontexts_A : It contains naive construction of context vectors.
		#wordcontexts_B : It involves the usage of similarity metric while computing the context vectors.
		#wordcontexts_large : It contains files from 11-150, otherwise its 11-39

	for m in range(11,39):
		fileName = "../testfiles_sm/tf00"+str(m)
		print fileName,
		MakeContextVec(fileName, wordVec, dim, wordID, validWords, tfidf, stopWords, simWords, selWords, window, fileList)
	
		print m, "IS DONE",
		if(m%3==0):
			print "\n",

	"""	
	for m in range(100,150):
		fileName = "../testfiles_sm/tf0"+str(m)
		print fileName,
		MakeContextVec(fileName, wordVec, dim, wordID, validWords, tfidf, stopWords, simWords, selWords, window, fileList)
	
		print m, "IS DONE",
		if(m%3==0):
			print "\n",
	"""
	
	for j in selWords:
		fileList[j].close()
	
	print i, "IS DONE"