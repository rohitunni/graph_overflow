import networkx as nx
from nxpd import draw
import numpy as np
import pandas as pd
from preprocessing import Preprocessor
from featurizer import Featurizer
from sklearn.metrics.pairwise import cosine_distances
from scipy.spatial.distance import cosine as cos_dist

class Graph_Overflow(object):

    def __init__(self, ncode_features = 10, code_features = 10, threshold = 1):
        self.nc = ncode_features
        self.c = code_features
        self.qa = self.nc + self.c
        self.G = None
        self.distances = []
        self.threshold = threshold
        pass

    def get_similarities(self, data):
        edge_list = []
        for i, node in enumerate(data):
            for j, other_node in enumerate(data):
                best_node_dist = (None, 1)
                qualifying_edges = []
                if i != j:
                    dist = cos_dist(node[self.qa:], other_node[:self.qa])
                    if dist < self.threshold:
                        qualifying_edges.append((i, j, dist))
                        self.distances.append(dist)

        return edge_list


    def make_digraph(self, data, ipynb = False):
        edge_list = self.get_similarities(data)
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)

        return self.G

    def prune_edges(self, edge_list):


        pass

    def draw_graph(self):
        if self.G == None:
            print 'Not fitted yet!'
            return
        else:
            nx.draw(self.G)
