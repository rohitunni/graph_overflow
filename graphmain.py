import snap
import gensim
from gensim import models, similarities
import json
from graph_creator import QA_Graph
from time import time

t = time()

lda_nc = models.ldamulticore.LdaMulticore.load('lda_noncode')
lda_c = models.ldamulticore.LdaMulticore.load('lda_code')

print "Loaded LDA models! :)"

with open('nc_question_corp.json', 'rb') as fa:
    nc_question = json.load(fa)

with open('nc_answer_corp.json', 'rb') as fb:
    nc_answer = json.load(fb)

with open('c_question_corp.json', 'rb') as fc:
    c_question = json.load(fc)

with open('c_answer_corp.json', 'rb') as fd:
    c_answer = json.load(fd)

print "Loaded jsons! :)"

print time() - t

qa_graph = QA_Graph(nc_question= nc_question, c_question = c_question,
                    nc_answer = nc_answer, c_answer = c_answer, num_edges = 200)


qa_graph.make_graph(lda_nc, lda_c, notif_num = 50, start = 0, stop = 1000)

G = qa_graph.g

print "Made graph"

print time() - t

FOut = snap.TFOut("graph_0_1000.graph")
G.Save(FOut)
FOut.Flush()
