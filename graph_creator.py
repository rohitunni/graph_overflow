import snap
import gensim
from gensim import models, similarities, corpora
from gensim.matutils import hellinger
from itertools import izip_longest

class QA_Graph(object):

    def __init__(self, nc_question, c_question,
                 nc_answer, c_answer, num_edges = 400, graph = None):
        self.nc_question = nc_question
        self.c_question = c_question
        self.nc_answer = nc_answer
        self.c_answer = c_answer
        self.num_edges = num_edges

        if graph == None:
            self.g = snap.TNGraph.New()
            self.size = len(self.nc_question)
            for i_node in range(self.size):
                self.g.AddNode(i_node)
            print "Initialized graph!"
        else:
            self.g = graph

    def make_graph(self, lda_nc, lda_c, notif_num = 20000, start = 0, stop = 500000):
        print "Starting to make indexes"

        index_nc = similarities.docsim.MatrixSimilarity(lda_nc[self.nc_question],
                                                        num_best = self.num_edges, num_features = 50)
        print "First index done!"
        index_c = similarities.docsim.MatrixSimilarity(lda_c[self.c_question],
                                                       num_best = self.num_edges), num_features = 50)

        print "Made similarity indexes!"

        for node_a, (ans_nc, ans_c) in enumerate(zip(self.nc_answer[start:stop], self.c_answer[start:stop]), start):

            query_anc = lda_nc[ans_nc]
            query_ac = lda_c[ans_c]

            sims_c = index_c[query_ac]

            sims_nc = index_nc[query_anc]

            "Made queries and similarities"

            for non_code_sim, code_sim in izip_longest(sims_nc, sims_c, fillvalue=(None, 0)):
                if non_code_sim[1] > 0 and node_a != non_code_sim[0]:
                    self.g.AddEdge(node_a, non_code_sim[0])
                if code_sim[1] > 0 and node_a != code_sim[0]:
                    self.g.AddEdge(node_a, code_sim[0])


            if node_a % notif_num == 0:
                print "Finished {}".format(node_a)







        print "Done!"

    def split_corpora(self, corpus_nc, corpus_c):
        n_nc = int(1.*len(corpus_nc)/2)
        n_c = int(1.*len(corpus_c)/2)

        q_nc = corpus_nc[:n_nc]
        a_nc = corpus_nc[n_nc:]

        q_c = corpus_c[:n_c]
        a_c = corpus_c[n_c:]

        return q_nc, a_nc, q_c, a_c
