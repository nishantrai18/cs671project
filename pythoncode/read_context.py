import numpy as np

def GetContexts (fileName):
	contextList = []
	with open(fileName,"r") as f:																#Read the context vectors from the file
		for line in f:
			numList = line.strip().split(' ')
			wordVector = []
			for x in numList:
				wordVector.append(float(x))
			wordVector = np.array(wordVector)
			contextList.append(wordVector)
	return contextList