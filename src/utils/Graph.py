import networkx as nx


class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def create_graph_from_blocks(self, output_text):
        self.graph.add_node('start')
        relations = output_text.split('---------------')
        for relation in relations:
            if not '->' in relation:
                continue

            u, v = relation.strip().split('->')
            self.graph.add_node(u)
            self.graph.add_node(v)
            self.graph.add_weighted_edges_from([(u, v, 1)])
