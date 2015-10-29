import numpy as np

from read_word import *

def PrecisionLimit (num):
	return "%.2f" % num

def CleanWord (word):
	symbols = [',','\"',"\'",".","?","/","(",")"]
	for c in symbols:
		word = word.replace(c,'')
	return word.lower()

def MakeContextVec (fileName, wordVec, dim, wordID,  											
					validWords, tfidf, stopWords, 
					selWords, window, fileList):												#tfidf's, words to be considered as input
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
								#print (tfidf[sentence[j]])
								#print (wordVec[wordID[sentence[j]]])
								wordVector = wordVector + (tfidf[sentence[j]]*wordVec[wordID[sentence[j]]])
					if (wordVector.dot(wordVector) > 0):
						for k in range(0,len(wordVector)):
							fileList[sentence[i]].write(str(PrecisionLimit(wordVector[k]))+" ")
					fileList[sentence[i]].write("\n")

wordVec = {}																		#Takes integer as argument and maps it to a word vector
wordID = {}																			#Takes a word and maps it to an id 
numIDS = {}																			#Inverse mapping for wordVec
dim = 0

#wordVec, wordID, numIDS, dim = GetWordVec("../googvecs")
wordVec, wordID, numIDS, dim = GetWordVec("../huang50rep")

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
print wordVec.keys()[:100] 	

multiList = []
vocabID = {}
invVocab = {}
numIDS = 0

trimNum = 1000																		#Get the number of words to consider
																					#Create the trimmed list of words
for i in range(0,trimNum):
	if (wordFreq[i] in validWords):
		multiList.append(wordFreq[i])

sz = len(multiList)

#print multiList

print "SIZE IS ", sz

np.set_printoptions(precision=2)															#Pretty print
np.set_printoptions(suppress=True)

#Construct the context vectors

#First open the files of a couple of words
#We first read the files piece wise (Since they are broken into multiple pieces)
#We go over the file and compute the corresponding context vector for it
#We append the context vector for a word in a file named <word>.cont
#We compute the vectors of only the words which have their files open

i = 0
window = 5

while (i < trimNum):
	wordSlice = multiList[i:i+100]
	selWords = []

	for w in wordSlice:
		if (w.isalpha()):
			selWords.append(w)
	i += 100

	fileList = {}
	for j in selWords:
		fileList[j] = open("wordcontexts"+str(dim)+"d/"+j+".cont", "a")

	for m in range(11,30):
		fileName = "../testfiles_sm/tf00"+str(m)
		print fileName
		MakeContextVec(fileName, wordVec, dim, wordID, validWords, tfidf, stopWords, selWords, window, fileList)
	
		print m, "IS DONE",

	for j in selWords:
		fileList[j].close()
	
	print i, "IS DONE",