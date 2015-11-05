import numpy as np

def GetWordVec(fileName):																#Takes fileName, returns dict of word vectors
																						#Also, gives a mapping/revmapping from words
																						#to integers

	wordVec = {}																		#Takes integer as argument and maps it to a word vector
	wordID = {}																			#Takes a word and maps it to an id 
	invID = {}																			#Inverse mapping for wordVec
	numIDS = 0
	numWord = 0
	dim = 0

	with open(fileName,"r") as f:																#Read the word vectors from the file
		for line in f:
			wordList = line.strip().split(' ')
			if (len(wordList) < 3):
				numWord, dim = int(wordList[0]),int(wordList[1])
			else:	
				word = wordList[0]
				wordID[word] = numIDS
				invID[numIDS] = word
				numIDS += 1
				wordVector = []
				for x in range(1, dim+1):
					y = float(wordList[x])
					wordVector.append(y)
				wordVec[wordID[word]] = np.array(wordVector)

	return wordVec, wordID, invID, dim

def GetWordFile (fileName, excluded):													#Takes fileName and a list of words not to be included

	wordSet = []

	with open(fileName,"r") as f:																#Get a wordList of frequent words in order
		for line in f:
			wordList = line.strip().split(' ')
			if (wordList[0] not in excluded):
				wordSet.append(wordList[0])

	return wordSet																		#Returns list of extracted words

def GetMultiWordVec(fileName):																#Takes fileName, returns dict of word vectors
																							#with multiple senses i.e. a list of cluster senses
																							#Also, gives a mapping/revmapping from words
																							#to integers

	wordVec = {}																		#Takes integer as argument and maps it to a word vector
	wordID = {}																			#Takes a word and maps it to an id 
	invID = {}																			#Inverse mapping for wordVec
	numIDS = 0
	numWord = 0
	dim = 0
	currentSense = 0

	with open(fileName,"r") as f:																#Read the word vectors from the file
		for line in f:
			wordList = line.strip().split(' ')
			if (len(wordList) <= 1):
				currentSense = int(wordList[0])
			elif (len(wordList) <= 3):
				numWord, numSenses, dim = int(wordList[0]),int(wordList[1]),int(wordList[2])
				wordVec[wordID[word]] = []
				currentSense = 0
			else:
				wordID[word] = numIDS
				invID[numIDS] = word
				numIDS += 1
				wordVector = []
				for x in range(0, dim):
					y = float(wordList[x])
					wordVector.append(y)
				wordVec[wordID[word]].append(np.array(wordVector))

	return wordVec, wordID, invID, dim