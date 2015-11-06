import numpy as np
import math

from read_word import *

def PrecisionLimit (num):
	return "%.3f" % num

def Normalize (v):
    norm = np.sqrt(v.dot(v))
    if (norm == 0): 
       return v, 0
    return (v/norm), 1

def CleanWord (word):
	symbols = [',','\"',"\'",".","?","/","(",")",";"]
	for c in symbols:
		word = word.replace(c,'')
	return word.lower()

def sigmoid(x):
	return 1 / (1 + math.exp(-x))

def CosineSimilarity (vecA, vecB):
	dot = vecA.dot(vecB)
	normA = np.sqrt(vecA.dot(vecA))
	normB = np.sqrt(vecB.dot(vecB))
	similarity = (dot/(normA*normB))
	return similarity

def sim (wA, wB, wordVec, wordID):									#Gives the cosine similarity
	vecA = wordVec[wordID[wA]]
	vecB = wordVec[wordID[wB]]
	similarity = CosineSimilarity(vecA, vecB)
	return sigmoid(similarity)

def ConstructContextVec (sentence, position, window, dim, wordVec, wordID, validWords, tfidf, stopWords):					#Returns the context vector along with the
																															#words used to construct it
	wordVector = np.zeros(dim)			
	wordList = []
	#print "THE BIG WORD IS ", sentence[position],
	for j in range(position-window, position+window):
		if (j < 0):
			j = -1
		elif (j >= len(sentence)):
			break
		elif (j == position):
			continue
		elif (sentence[j] in validWords):											#Checks if present in vocabulary
			if(sentence[j] not in stopWords):
				#print sentence[j],
				if (tfidf[sentence[j]] > 0):
					wordVector = wordVector + \
					(tfidf[sentence[j]]*sim(sentence[position], sentence[j], wordVec, wordID))*wordVec[wordID[sentence[j]]]					
																				#Change here to alter the construction of context vectors
					wordList.append(sentence[j])
	return wordVector, wordList

def MakeContextVec (fileName, wordVec, dim, wordID,  											
					validWords, tfidf, stopWords,										
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
					wordVector, tmp = ConstructContextVec(sentence, i, window, dim, wordVec, wordID, validWords, tfidf, stopWords)								
					if (wordVector.dot(wordVector) > 0):
						wordVector, status = Normalize(wordVector)
						if (status == 0):
							continue
						for k in range(0,len(wordVector)):
							fileList[sentence[i]].write(str(PrecisionLimit(wordVector[k]))+" ")
						fileList[sentence[i]].write("\n")

def MakeContextVecWithGoodWords (fileName, wordVec, dim, wordID,  											
								validWords, tfidf, stopWords,									
								selWords, window, fileList):												#tfidf's, words to be considered as input
																											#simWords is a dictionary with similarities
																											#window is the length considered to the left and right
																											#vocabID is the vocabulary integer mapping 
	with open(fileName,"r") as f:																			#Read the word vectors from the file
		for line in f:
			sentence = line.strip().split(' ')																#Get a list of words
			for i in range(0, len(sentence)):
				sentence[i] = CleanWord(sentence[i])
			for i in range (0, len(sentence)):
				if (sentence[i] in selWords):													#If current word is in the context list
					wordVector, wordList = ConstructContextVec(sentence, i, window, dim, wordVec, wordID, validWords, tfidf, stopWords)								
					if (wordVector.dot(wordVector) > 0):
						wordVector, status = Normalize(wordVector)
						if (status == 0):
							continue
						fileList[sentence[i]].write(str(len(wordList))+" ")
						for w in wordList:
							fileList[sentence[i]].write(w+" ")
						fileList[sentence[i]].write("\n")
						for k in range(0,len(wordVector)):
							fileList[sentence[i]].write(str(PrecisionLimit(wordVector[k]))+" ")
						fileList[sentence[i]].write("\n")

def AssignCluster(wordVector, multiWordVector):									#wordVector is the computed word Vector,
																				#multiWordVector gives the vectors of the many senses
	ID = 0
	maxSim = 0
	for i in range(0,len(multiWordVector)):
		tmp = CosineSimilarity(wordVector, multiWordVector[i])
		if (tmp > maxSim):
			maxSim = tmp
			ID = i
	return ID