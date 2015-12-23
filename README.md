Repository for CS671A project:
------------------------------

The project deals with the problem of construction of Multiple Sense Embeddings for different words. We develop several models to tackle the problem consisting of Online Clustering Methods, Methods involving Parameter Estimation and also look at methods related to Word Word Co-occurrence matrices. The training data used is the April 2010 snapshot of the Wikipedia corpus. Our model uses the popular Word2vec tool to compute Single Word Embeddings. We compare the performance of our approaches with current state of the art models and find that our model is comparable to the state of the art models and even outperforms them in some cases. Our model is extremely efficient and takes less than 6 hours for complete training and computation of senses. We also discuss the possibility of our model giving better (semantically coherent) senses than present models. The main task used for comparing the models is the SCWS task. The comparisons have been done using human judgment of semantic similarity.


Project Report, Code, Poster and more details available at : http://home.iitk.ac.in/~nishantr/cs671/project/

The structure of the project code is as follows,
- pythoncode : Conatins the python version of computing multiple sense embeddings
- Rest : Contains codes in C++ (Due to need for speed), especially in the online clustering algorithms.
- Driver programs : General programs which are used by both python and cpp versions, for example, compsim.cpp (For SCWS Task), word2vec (For computing embeddings)

The details about the python implementation are provided in the folder. 

The C++ version is described as follows,
- iter_npms.cpp : Runs the iterative version of the Online Clustering
- npmssr.cpp : The original version of the clustering algorithm. Clustering is done online, the number of clusters are varied on the basis of the new point.

The driver functions are briefly described below,
- word2vec.c : Contains the implemetation of the popular word2vec tool by Mikolov et al.
- compsim.cpp : Runs the SCWS test on the given vectors. Contains multiple metrics for comparison.
