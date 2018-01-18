import snap
import gensim
from gensim import models, similarities
import pickle
from stack_nextchange.graph_creator import QA_Graph
from time import time

lda_nc = models.ldamulticore.LdaMulticore.load('lda_noncode')
lda_c = models.ldamulticore.LdaMulticore.load('lda_code')

print "Loaded LDA models! :)"

with open('ncode_corp_dict.pkl', 'rb') as fnc:
    noncode_pickle = pickle.load(fnc)

with open('code_corp_dict.pkl', 'rb') as fc:
    code_pickle = pickle.load(fc)

corpus_nc = noncode_pickle[0]
corpus_c = code_pickle[0]

print "Loaded pickles! :)"

qa_graph = QA_Graph(threshold = 0.1, corp_nc = corpus_nc, corp_c = corpus_c, start = 0, stop = 10000)

t = time()

qa_graph.make_graph(lda_nc, lda_c, notif_num = 50)

G = qa_graph.g

print "Made graph"

print time() - t

FOut = snap.TFOut("firstgraph.graph")
G.Save(FOut)
FOut.Flush()
