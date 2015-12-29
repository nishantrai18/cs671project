Python Implementation for computing Multiple Word Embeddings:
-------------------------------------------------------------

The descriptions of the files are as shown below,
- recreate_data.py : Reconstruct the files by replacing each word by its probable sense. Requires sense clusters to be already computed.
- read_word.py : Contains several functions for reading files, getting word statistics
- reader.py : Test file demonstrating construction of word word cooccurence matrix from multiple files (i.e. In parts)
- read_context.oy : Function to extract context of a word
- get_senses.py : Contains essence of the whole project. Functions for parametric, non parametric clustering. Also includes function to plot the final word vectors using TSNE.
- param_senses.py : Driver program for performing parametric word sense estimation
- multiword_tsne.py : Plot reduced space for Multiple Senses Word Vectors (Uses TSNE)
- make_cont.py : Creates context file for different words. Slightly optimized for speed using multiple file pointers. Output written to multiple files, named after the word it corresponds to.
- good_words.py : Roughly the same as make_cont.py, but differs in the output files. It also outputs the good words (Based on Negative Sampling) along with the contexts.
- create_contexts.py : Contains functions for computing contexts, estimating senses, etc
- xmeans.py : Implementation of XMeans algorithm
- wwclustering_rcm.py : Includes code for Reverse McKee Hill Ordering. Finally plots the word coocurrence matrix after re ordering.
