import networkx as nx
import matplotlib.pyplot as plt
from random import sample
#from networkx.algorithms.tournament import hamiltonian_path


def draw_graph(G, labels=None, graph_layout='spring',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=9,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    '''
    From SO - graph drawing function from NetworkX
    '''

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos = nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos = nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos = nx.random_layout(G)
    else:
        graph_pos = nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G, graph_pos, node_size=node_size,
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G, graph_pos, width=edge_tickness,
                           alpha=edge_alpha, edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos, font_size=node_text_size,
                            font_family=text_font)

    # if labels is None:
        # labels = range(len(graph))

    # edge_labels = dict(zip(graph, labels))
    # nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels,
    #                             label_pos=edge_text_pos)

    # show graph
    plt.show()


def get_graph_from_edges(list_of_player_edges):
    '''
    From the directed list of player-edge tuples, generate a directed
    graph (DiGraph)
    '''
    G = nx.DiGraph()

    # add edges
    for edge in list_of_player_edges:
        G.add_edge(edge[0], edge[1])

    return G


def get_hamiltonian_path_from_graph(G):
    return hamiltonian_path(G)


def is_there_definitely_no_hamiltonian_cycle(G):
    nodes = G.nodes()
    for node in nodes:
        # If some node only has one neighbour - NO HAM-CYCLE EXISTS
        if len(G.neighbors(node)) <= 1:
            print "Node has <= 1 neighbour: %s" % str(node)
            return True

    return False



def get_one_full_cycle_from_graph(G):
    number_of_nodes = nx.number_of_nodes(G)
    nodes = G.nodes()
    cycles = nx.simple_cycles(G)

    for idx, cycle in enumerate(cycles):
        cycle_length = len(cycle)

        if idx % 10000 == 0:
            print "Processing cycle: %s with length %s | expecting length %s" % (str(idx), str(cycle_length), str(number_of_nodes))
            remaining_nodes = set(nodes).difference(cycle)
            print "Remaining nodes: %s\n" % str(remaining_nodes)

        if cycle_length == number_of_nodes:
            print "Solution found at cycle %s with length %s" % (str(idx), str(cycle_length))
            return cycle

    return None


def get_full_cycles_from_graph(G):
    cycles = list(nx.simple_cycles(G))
    number_of_nodes = nx.number_of_nodes(G)
    if number_of_nodes != 0:
        print "Number of nodes in cycle: %s" % number_of_nodes
        full_cycles = filter(lambda cycle: len(cycle) == number_of_nodes, cycles)
        return full_cycles
    else:
        return None


def full_cycle_to_edges(full_cycle):
    # Iterate from first element to last minus one
    # Since we want grouping of two
    edges_in_full_cycle = []
    for i in xrange(0, len(full_cycle) - 1):
        edges_in_full_cycle.append((full_cycle[i], full_cycle[i + 1]))

    # Link the first and last two nodes as well
    edges_in_full_cycle.append((full_cycle[len(full_cycle) - 1], full_cycle[0]))
    return edges_in_full_cycle


def get_one_full_cycle(full_cycles):
    if full_cycles is not None and len(full_cycles) > 0:
        full_cycles = sample(full_cycles, len(full_cycles))
        full_cycle = full_cycles[0]
        print "Full cycle found: %s" % full_cycle
        return full_cycle


def convert_full_cycle_to_graph(full_cycle):
    '''
    Get a graph representation of one cycle from a list of full cycles
    '''
    edges_in_full_cycle = full_cycle_to_edges(full_cycle)
    g2 = get_graph_from_edges(edges_in_full_cycle)
    return g2


if __name__ == "__main__":
    graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9),
             (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]

    # you may name your edge labels
    labels = map(chr, range(65, 65 + len(graph)))
    # draw_graph(graph, labels)

    # if edge labels is not specified, numeric labels (0, 1, 2...) will be used
    draw_graph(graph)
