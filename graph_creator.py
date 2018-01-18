import snap
import gensim
from gensim import models, similarities, corpora
from gensim.matutils import hellinger

class QA_Graph(object):

    def __init__(self, threshold, corp_nc, corp_c, graph = None):
        self.corp_nc = corp_nc
        self.corp_c = corp_c
        self.threshold = threshold
        if graph == None:
            self.g = snap.TNGraph.New()
            self.size = int(1.*len(self.corp_nc)/2)
            for i_node in range(self.size):
                self.g.AddNode(i_node)
            print "Initialized graph!"
        else:
            self.g = graph

    def make_graph(self, lda_nc, lda_c, notif_num = 20000, start = 0, stop = 500000):
        q_nc, a_nc, q_c, a_c = self.split_corpora(self.corp_nc, self.corp_c)

        print "Split corpora"
        n = len(q_nc)

        for node_a, (ans_nc, ans_c) in enumerate(zip(a_nc[start:stop], a_c[start:stop]), start):
            for node_q, (ques_nc, ques_c) in enumerate(zip(q_nc, q_c)):
                if node_a != node_q:
                    qualifying_edges = []
                    best_other_edge = None
                    dist_nc = hellinger(lda_nc[ans_nc], lda_nc[ques_nc])
                    dist_c = hellinger(lda_c[ans_c], lda_c[ques_c])
                    avg_dist = 1.*(dist_nc + dist_c)/2
                    if avg_dist <= self.threshold:
                        qualifying_edges.append((node_a, node_q))
                    else:
                        if best_other_edge == None:
                            best_other_edge = (node_a, node_q, avg_dist)
                        elif avg_dist < best_other_edge[2]:
                            best_other_edge = (node_a, node_q, avg_dist)
            # Add all qualifying edges to the graph
            if len(qualifying_edges) > 0:
                for edge in qualifying_edges:
                    self.g.AddEdge(edge[0], edge[1])
            # If no edges qualify, sort the other edges
            else:
                self.g.AddEdge(best_other_edge[0], best_other_edge[1])

            if node_a % notif_num == 0:
                print 'Finished node {}!'.format(node_a)

        print "Done!"

    def split_corpora(self, corpus_nc, corpus_c):
        n_nc = int(1.*len(corpus_nc)/2)
        n_c = int(1.*len(corpus_c)/2)

        q_nc = corpus_nc[:n_nc]
        a_nc = corpus_nc[n_nc:]

        q_c = corpus_c[:n_c]
        a_c = corpus_c[n_c:]

        return q_nc, a_nc, q_c, a_c
