from unittest import TestCase
from dijkstra_shortest_path import DijkstraSearch, make_undirected_weighted_graph


class TestDijkstraSearch(TestCase):
    def test_find_shortest_paths(self):
        """
                Sample Input
                1
                4 4
                1 2 24
                1 4 20
                3 1 3
                4 3 12
                1

                Sample Output

                24 3 15
                """
        expected = '24 3 15'

        edges = [[1, 2, 24], [1, 4, 20], [3, 1, 3], [4, 3, 12]]
        s = 1
        g = make_undirected_weighted_graph(edges)
        dijkstra_search = DijkstraSearch(g)
        sorted_weights_str = dijkstra_search.str_of_sorted_shortest_paths(s)
        self.assertEqual(expected, sorted_weights_str)
