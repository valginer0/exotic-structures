"""
The standard Python heapq interface does not contain methods for efficient updates of
heap elements.   Dijkstra algorithm is an example where such functionality is useful.
This Python implementation of Heap contains method update() and a convenience method
decrease() to satisfy this additional requirement.

"""

from collections import namedtuple

HeapElement = namedtuple('HeapElement', ['heap_key', 'key', 'data'])


class UpdatableHeap(object):
    """
    As a clarifying example:
    when using the object of type UpdatableHeap in dijkstra_shortest_path module,
    the data members 'heap_key' and 'key' of HeapElement are set to a weight and node of a graph node respectively.

    Invariants: self.heap satisfies the heap invariant condition at the beginning and at the end of the methods.
    """

    ZERO_POZ = 0

    def __init__(self):
        self.heap = []
        self.register = {}

    def __len__(self):
        return len(self.heap)

    def push(self, heap_key, key, data):
        """
        Create a new heap element.
        :param heap_key:    when used in dijkstra, this is a weight of the node
        :param key:         when used in dijkstra, this is the node
        :param data:        this parameter is not used in dijkstra
        """
        el = HeapElement(heap_key, key, data)
        self.heap.append(el)
        idx = self.register[key] = len(self.heap) - 1
        self._bubble_up(idx)

    def pop(self):
        """
        Pop the head of the heap and fix internal accounting.
        :param heap_key:    when used in dijkstra, this is a weight of the node
        :param key:         when used in dijkstra, this is the node
        :param data:        this parameter is not used in dijkstra
        :return:            the head of the heap
        """
        self._swap_heap_and_register(self.ZERO_POZ, len(self.heap) - 1)
        del self.register[self.heap[-1].key]
        result_el = self.heap.pop()
        self._bubble_down(self.ZERO_POZ)
        return result_el

    def decrease(self, new_heap_key, key, data):
        """
        If no element with the key present in the heap, create it.  Otherwise,
        if the new_heap_key is less then the value of the heap_key for the key, replace heap_key with new_heap_key
        :param heap_key:    when used in dijkstra, this is a weight of the node
        :param key:         when used in dijkstra, this is the node
        :param data:        this parameter is not used in dijkstra
        """
        idx = self.register.get(key)
        if not idx:  # no element with the key is present in the heap, create it
            self.push(new_heap_key, key, data)
        else:
            self.heap[idx] = HeapElement(new_heap_key, key, data)
            pos = self._bubble_up(idx)  # may work only if new_heap_key is less than the old value of heap_key

    def update(self, new_heap_key, key, data):
        """
        For the given key, replace the self.heap that has the key=key with the new value of heap_key,
        after that fix the heap invariant.
        :param new_heap_key: new value of the heap_key, which in the case of Dijksra is a new wight for the node (key)
        :param key: value of key, which is in case of Dijkstra is the node
        :param data: value of data, which is no used in case of Dijkstra
        """
        idx = self.register[key]
        self.heap[idx] = HeapElement(new_heap_key, key, data)
        pos = self._bubble_up(idx)  # may work only if new_heap_key is less than the old value of heap_key
        if pos != idx:
            self._bubble_down(idx)  # get here only if new_heap_key is greater than the old value of heap_key

    def sorted_iterator(self):
        """
        Yield heap elements in sorted order
        """
        heap_store = self.heap[:]
        while self.heap:
            yield self.pop()
        self.heap[:] = heap_store

    def heapsort(self, lst):
        """
        Returns a sorted list, at the end it is converted to a heap
        :param lst: a list to be sorted
        :return: a sorted list
        """
        result, heap_store = [], []
        for x in lst:
            self.push(*x)
        heap_store = self.heap[:]
        while self.heap:
            x = self.pop()
            result.append((x.heap_key, x.key, x.data))
        self.heap = heap_store[:]
        return result

    def _bubble_up(self, pos):
        """
        Parent's index of j is (j-1)//2;
        Move the element in pos in the position where the heap invariant holds,
        while updating all the indexes in the registry for all the element moved in the process
        :param pos:
        :return: a new position of the element
        """
        while pos > self.ZERO_POZ:
            parent_idx = (pos - 1) >> 1
            pos_key = self.heap[pos].key
            if self.heap[parent_idx] <= self.heap[pos]:
                self.register[pos_key] = pos
                return pos
            self._swap_heap_and_register(pos, parent_idx)
            pos = parent_idx
        return pos

    def _bubble_down(self, pos):
        """
        Indexes of the children of k are 2*k+1 and 2*k+2;
        At the end, h satisfies the heap invariant.
        Exchange the element in pos with the smallest of its children if needed; continue until the invariant holds
        :param pos: pos of the element to bubble down
        :return: the final position of the element, when the heap invariant holds
        """
        while (pos << 1) + 1 < len(self.heap):
            chld_idx, chld2_idx = (pos << 1) + 1, (pos << 1) + 2
            min_chld_idx = (chld2_idx if (chld2_idx < len(self.heap)) and
                                         self.heap[chld2_idx] < self.heap[chld_idx] else chld_idx)
            if self.heap[pos] <= self.heap[min_chld_idx]:
                return pos
            self._swap_heap_and_register(pos, min_chld_idx)
            pos = min_chld_idx
        return pos

    def _swap_heap_and_register(self, idx, idx2):
        idx_key, idx2_key = self.heap[idx].key, self.heap[idx2].key
        self.register[idx2_key], self.register[idx_key] = idx, idx2
        self.heap[idx2], self.heap[idx] = self.heap[idx], self.heap[idx2]


if __name__ == '__main__':
    """
    Keeping some tests here as examples of the usage.
    Unit tests are also presented in the tests package.
    """


    def test_generic_heap_sort_case():
        l2 = [
            (5, 5, 5), (1, 1, 1), (3, 3, 3), (0, 0, 0), (10, 10, 10), (11, 11, 11), (9, 9, 9), (8, 8, 8), (7, 7, 7),
            (2, 2, 2), (6, 6, 6)
        ]
        expected = [
            (0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 3, 3), (5, 5, 5),
            (6, 6, 6), (7, 7, 7), (8, 8, 8), (9, 9, 9), (10, 10, 10), (11, 11, 11)
        ]
        heapq = UpdatableHeap()
        realised = heapq.heapsort(l2)
        assert expected == realised


    def test_generic_heap_update_case():
        l2 = [
            (5, 5, 5), (1, 1, 1), (3, 3, 3), (0, 0, 0), (10, 10, 10), (11, 11, 11), (9, 9, 9), (8, 8, 8), (7, 7, 7),
            (2, 2, 2), (6, 6, 6)
        ]
        expected = [
            (0, 0, 0), (1, 1, 1), (2, 2, 2), (5, 5, 5), (6, 6, 6), (7, 7, 7),
            (8, 8, 8), (9, 9, 9), (10, 10, 10), (11, 11, 11), (20, 3, 3),
        ]
        heapq = UpdatableHeap()
        for x in l2:
            heapq.push(*x)
        heapq.update(*(20, 3, 3))
        realised = [(x.heap_key, x.key, x.data) for x in heapq.sorted_iterator()]
        assert expected == realised


    def test_empty_heap_sort_case():
        l2 = []
        expected = []
        heapq = UpdatableHeap()
        realised = heapq.heapsort(l2)
        assert expected == realised


    test_empty_heap_sort_case()
    test_generic_heap_sort_case()
    test_generic_heap_update_case()

    # from timeit import timeit
    # t = timeit('from __main__ import test_generic_heap_update_case; test_generic_heap_update_case()', number=10000)
    # print(t)
