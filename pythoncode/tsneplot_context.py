from get_senses import *
from read_word import *

np.set_printoptions(precision=2)															#Pretty print
np.set_printoptions(suppress=True)

#cluster("bank",2,50)

dim = 50
fileName = "wordcontexts" + str(dim) + "d/" + "state" + ".cont"
data = GetContexts(fileName, dim)

ClusterPlot(data, 2)
PlotTSNE(data[:3000], [])