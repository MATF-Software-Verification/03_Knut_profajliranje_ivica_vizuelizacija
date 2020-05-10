import networkx as nx


class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def create_graph_from_blocks(self, output_text):
        self.graph.add_node('start')
        relations = output_text.split('---------------')
        for i in range(len(relations)):
            if '->' not in relations[i]:
                continue

            u, v = relations[i].strip().split('->')
            u = u.strip()
            v = v.strip()
            
            self.graph.add_node(u)
            if 0 == i:
                self.graph.add_weighted_edges_from([('start', u, 1)])

            self.graph.add_node(v)
            self.graph.add_weighted_edges_from([(u, v, 1)])

    def create_spanning_tree(self):
        return nx.minimum_spanning_tree(self.graph)

    def edges(self):
        return nx.edges(self.graph)

    def nodes(self):
        return nx.nodes(self.graph)



