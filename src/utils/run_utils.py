from src.utils.Graph import Graph


def main():
    g = Graph()
    g.create_graph_from_blocks('A\nB\n---------------\nC\nD')

if __name__ == '__main__':
    main()
