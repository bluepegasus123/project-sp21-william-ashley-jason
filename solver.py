import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    # Cities/Vertices we are planning on removing
    cities = []
    # Edges we are planning on removing
    edges = []

    size = len(list(G.nodes))

    # determine what the budget (c, k) of the graph is depending on the size of the graph
    if size >= 20 or size <= 30:
        budget_c = 1
        budget_k = 15
    elif size >= 31 or size <= 50:
        budget_c = 3
        budget_k = 50
    else:
        budget_c = 5
        budget_k = 100

    # We want to calculate what the shortest path is initially because any edge that we remove would ideally maximize
    # this shortest path length
    shortest_path_len = nx.dijkstra_path_length(G, 0, len(list(G.nodes)) - 1)
    #print("original shortest path len: ", shortest_path_len)
    #Creating shallow copy of our graph input to avoid changing the actual graph itself
    G_prime = G.copy()

    # We want to iterate through the number of edges we can possibly remove depending on our budget
    # We remove edges by a greedy approach:
    # Remove an edge, if the edge removal increases our shortest path distance,
    # we continue by updating shortest_path_len
    # to our improved shortest path length
    # Append that removed edge to our edges list that we will eventually return
    for edge in range(budget_k):

        # Helper function finds the edge which's removal will give the maximum shortest length
        ret = helper(G_prime)
        if ret == []:
            break
        G_prime = ret["G"]
        length = ret["max_path_len"]
        #print("possibly updating shortest path len to: ", length)
        if length <= shortest_path_len:
            break
        else:
            shortest_path_len = length
            #print("appending edge: ", ret["max_path_edge"])
            edges.append(ret["max_path_edge"])
    return cities, edges


def helper(G):

    # s is vertex 0, t is vertex |V| - 1
    s = 0
    t = len(G.nodes) - 1

    # lengths is a dictionary that keeps track of each edge that we iteratively remove and the corresponding
    # shortest path length from s to t once that edge has been removed
    # key = edge, value = path length
    lengths = {}
    G_copy = G.copy()
    # We explore all edges of the graph, and iteratively remove each one of them and run shortest paths
    for edge in list(G.edges):
        G_copy.remove_edge(edge[0], edge[1])

        try:
            path_len = nx.dijkstra_path_length(G_copy, s, t)
            # add edge, path length key value pair in dictionary to keep track of edge removal + path length
            lengths[edge] = path_len
            # "resetting" G_copy to be the original G passed in every time
            G_copy = G.copy()

        except:
            # Disconnected graph - path doesn't exist edge case
            continue

    # sort our dictionary based on its values - we want to remove the edge that gives maximum shortest path len
    # Check for empty lengths list here - NONE of our edges could be removed
    # DEBUG HERE - indexing error

    if len(lengths) == 0:
        return []

    sorted_lengths = sorted(lengths.items(), key = 
             lambda item:item[1], reverse=True)
    # sorted_lengths = sorted(lengths, lengths.get, True)
    # sorted_iterator = iter(sorted_lengths.keys())
    # print("Sorted lengths list", sorted_lengths)

    first_key = sorted_lengths[0][0]

    max_path_len = sorted_lengths[0][1]
    max_path_edge = first_key

    # things to add + things to check:
    # make sure the edge we're removing doesn't disconnect the graph
    # if it does take the next edge that gives you the next maximum shortest path length
    # key = next(sorted_iterator) to get the next maximum edge

    # remove the edge from our graph that gives the maximum shortest path distance
    G.remove_edge(max_path_edge[0], max_path_edge[1])

    ret = {"G": G, "max_path_len": max_path_len, "max_path_edge": max_path_edge}

    return ret

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in


if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    # folder =sys.argv[2]
    G = read_input_file(path)
    c, k = solve(G)
    assert is_valid_solution(G, c, k)
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    write_output_file(G, c, k, 'outputs/' + path.replace(".in", ".out").replace("/inputs", ""))


# # For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
