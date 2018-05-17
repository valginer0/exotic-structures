"""
This is a relatively fast implementation of classical Dijkstra short path algorithm:
it uses the UpdatableHeap implementation of the heap, which updates (decreases) values
of an internal element in logarithmic time, instead of sorting the whole heap each time
(e.g., as the implementation from the standard Python library heapq)

"""
from heap_with_update import HeapElement, UpdatableHeap
from collections import defaultdict


class WeightedGraph(object):
    def __init__(self, lst_of_vertices, adj_list):
        self.v = lst_of_vertices
        self.adj_list = adj_list


######################################################################################
class DijkstraSearch(object):
    def __init__(self, g):
        self.g = g
        self.queue = UpdatableHeap()
        self.prev = set()
        self.vds = {}

    def init_q(self, s):
        for v in self.g.v:
            if v != s:
                vd = HeapElement(heap_key=float('inf'), key=v, data=None)
                self.queue.push(*vd)
            else:
                vd = HeapElement(heap_key=0, key=s, data=None)
                self.queue.push(*vd)
            self.vds[vd.key] = vd

    def find_shortest_paths(self, s):
        vd = HeapElement(heap_key=0, key=s, data=None)
        self.queue.push(*vd)
        self.vds[vd.key] = vd

        while len(self.queue):
            current = self.queue.pop()
            self.prev.add(current.key)
            for (u, weight) in self.g.adj_list[current.key].items():
                if (u not in self.prev):
                    if ((not self.vds.get(u)) or
                            (self.vds.get(u) and (current.heap_key + weight < self.vds[u].heap_key))):
                        new_heap_key = current.heap_key + weight
                        self.vds[u] = HeapElement(heap_key=new_heap_key, key=u, data=None)
                        self.queue.decrease(*self.vds[u])

        sorted_vertices = sorted(self.vds.keys())
        sorted_weights = [self.vds[v].heap_key if v in sorted_vertices else '-1' for v in self.g.v if v != s]
        return sorted_weights

    def str_of_sorted_shortest_paths(self, s):
        sws = self.find_shortest_paths(s)
        return ' '.join([str(w) if w != float('inf') else '-1' for w in sws])


######################################################################################

def make_undirected_weighted_graph(edges):
    """
    A convenience function, which if needed, converts a graph to undirected graph,
    also if there are two edge with different weights, only the one with the smaller weights
    would be left in the output.  This wouldn't change the dijkstra result

    :param edges: an iterable containing triples node1,node2,weight;
    :return: adjacency list of the resulting graph
    """
    adj_list = defaultdict(dict)
    for edge in edges:
        x, y, r = edge
        if (x not in adj_list) or (y not in adj_list[x]):
            adj_list[x][y] = r
        else:
            w = min(adj_list[x][y], r)
            adj_list[x][y] = w
        if (y not in adj_list) or (x not in adj_list[y]):
            adj_list[y][x] = r
        else:
            w = min(adj_list[y][x], r)
            adj_list[y][x] = w

    lst_of_vertices = sorted(adj_list.keys())
    return WeightedGraph(lst_of_vertices, adj_list)
