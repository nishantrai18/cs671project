import numpy as np
import math

from read_word import *
from get_senses import *
from create_contexts import *

def AssignCluster(word, wordVector, multiWordVec, multiWordID):
	if word in multiWordID:
		multiWordVector = multiWordVec[multiWordID[word]]
		ID = 0
		maxSim = 0
		for i in range(0,len(multiWordVector)):
			tmp = CosineSimilarity(wordVector, multiWordVector[i])
			if (tmp > maxSim):
				maxSim = tmp
				ID = i
		return ID
	else:
		return -1

wordVec, wordID, numIDS, dim = GetWordVec("../neel50d6K")

multiWordVec, multiWordID, multiNumIDS, dim = GetMultiWordVec("multisense/multisenses3n50d_neelB.vec")	

print "INPUT WORD VECTORS/ MULTISENSE VECTORS COMPLETE"

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

raw_input("RECONSTRUCT FILES FOR FURTHER TRAINING (Y/N) : ")

print "GETTING TFIDF COMPLETE"														#Getting list of stopwords	

multiList = []
trimNum = 6000																		#Get the number of words to consider
																					#Create the trimmed list of words
for i in range(0,trimNum):
	if (wordFreq[i] in validWords):
		multiList.append(wordFreq[i])

sz = len(multiList)

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

#Re construct the training files

#We first read the files piece wise (Since they are broken into multiple pieces)
#We go over the file and compute the corresponding context vector for the valid words
#We get an idea of which cluster the word belongs to, and replace it by "<word>_<num>"

i = 0																		#Starting point

window = 5

for m in range(11,12):
	fileName = "../testfiles_sm/tf00"+str(m)
	newFileName = "../trainfiles_neel6K/tf00"+str(m)

	fw = open(newFileName, "w")

	print fileName, newFileName
	
	with open(fileName,"r") as f:																						#Read the word vectors from the file
		for line in f:
			sentence = line.strip().split(' ')																			#Get a list of words
			cleanSentence = []
			for i in range(0, len(sentence)):
				cleanSentence.append(CleanWord(sentence[i]))
			for i in range (0, len(cleanSentence)):
				if (cleanSentence[i] in multiList):																		#If current word is in the context list
					wordVector = ConstructContextVec(cleanSentence, i, window, dim, wordVec, wordID, validWords, tfidf, stopWords)								
					if (wordVector.dot(wordVector) > 0):
						wordVector, status = Normalize(wordVector)
						if (status == 0):
							continue
						clusterID = AssignCluster(cleanSentence[i], wordVector, multiWordVec, multiWordID)
						if (clusterID >= 0):
							sentence[i] = cleanSentence[i] + "_" + str(clusterID)		
			for k in range(0,len(sentence)):
				fw.write(sentence[k]+" ")
			fw.write("\n")			

	print m, "IS DONE",
	if(m%3==0):
		print "\n",