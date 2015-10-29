import numpy as np
import scipy.sparse as sp
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

filename = "googvecs"

wordvec = {}																		#Takes integer as argument and maps it to a word vector
wordid = {}																			#Takes a word and maps it to an id 
invid = {}																			#Inverse mapping for wordvec
ids = 0

with open(filename,"r") as f:																#Read the word vectors from the file
	numword = 0
	dim = 0
	for line in f:
		lis = line.strip().split(' ')
		if (len(lis) < 3):
			numword, dim = int(lis[0]),int(lis[1])
		else:	
			word = lis[0]
			wordid[word] = ids
			invid[ids] = word
			ids+=1
			vector = []
			for x in range(1, dim+1):
				y = float(lis[x])
				vector.append(y)
			wordvec[wordid[word]] = vector

filename = "stopwords"

stops = []

with open(filename,"r") as f:																#Get a list of frequent words in order
	for line in f:
		lis = line.strip().split(' ')
		stops.append(lis[0])

wfreq = []

#print stops

filename = "vocab.txt"

with open(filename,"r") as f:																#Get a list of frequent words in order
	for line in f:
		lis = line.strip().split(' ')
		if (lis[0] not in stops):
			wfreq.append(lis[0])

#print wfreq[:100]
#print wordvec.keys()[:100] 	

smlist = []
vocabid = {}
invocab = {}
ids = 0

num = 1000																					#Create the trimmed list of words
for i in range(0,num):
	if (wfreq[i] in wordid):
		smlist.append(wfreq[i])
		vocabid[wfreq[i]] = ids																#Stores the id of the trimmed words
		invocab[ids] = wfreq[i]																#The inverse mapping
		ids += 1

sz = len(smlist)

#print smlist

print "SIZE IS ", sz

np.set_printoptions(precision=2)															#Pretty print
np.set_printoptions(suppress=True)

mat = np.zeros((sz,sz))																		#Cooccurence matric of the trimmed words
	
#Build the word word coocurence matrix/ Construct the context vectors

for ti in range(11,40):
	filename = "testfiles_sm/tf00"+str(ti)
	print filename

	with open(filename,"r") as f:																#Read the word vectors from the file
		for line in f:
			lis = line.strip().split(' ')
			sent = []
			for x in lis:
					sent.append(x)
			window = 5																			#Refers to word considered to the left and to the right

			for i in range(0,len(sent)):
				if (sent[i] in vocabid):
					for j in range(i-window,i+window):
						if (j < 0):
							j = -1
						elif (j >= len(sent)):
							break
						elif (j==i):
							continue
						elif (sent[j] in vocabid):
							mat[vocabid[sent[i]]][vocabid[sent[j]]] += 1

	print ti, "IS DONE",


vals = []

for r in mat:
	for c in r:
		vals.append(c)

vals.sort()

key = vals[(int)((0.95)*(len(vals)))]

print key

mat[ mat < key ] = 0
mat[ mat >= key ] = 1

#mat /= mat.max()

print mat

imgplot = plt.imshow(mat, cmap='Greys', interpolation='nearest')

plt.show()

graph = sp.csr_matrix(mat)

order = sp.csgraph.reverse_cuthill_mckee(graph)

nmat = mat[order][:,order]

print order

print nmat

imgplot = plt.imshow(nmat, cmap='Greys', interpolation='nearest')

plt.show()
