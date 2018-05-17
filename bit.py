"""
Binary Indexed Tree AKA Fenwick Tree

references:
https://www.youtube.com/watch?v=v_wj_mOAlig&t=1s
https://cs.stackexchange.com/questions/10538/bit-what-is-the-intuition-behind-a-binary-indexed-tree-and-how-was-it-thought-a


"""


class BITError(Exception):
    pass


class Bit(object):
    """
    Implementation of Binary Index Tree AKA Fenwick Tree.
    Internally, using indexes in the range(1,n+1) to enable specific BIT indexing trick
    """

    def __init__(self, n):
        """
        Moved initialisation into init_with_list() method for convenience.
        Don't forget to always use init_with_list() method first.
        """
        if n < 1:
            raise BITError('Illegal input length')

        self.tree_lst = [0] * (n + 1)

    def init_with_list(self, lst):
        """

        This implementation requires O(n*lg(n))  operations.
        :param lst: the list to initialize the tree with
        :return:
        """
        n = len(lst)
        if n < 1:
            raise BITError('Illegal input length')
        self.tree_lst = [0] * (n + 1)
        for j, x in enumerate(lst):
            self.add_at(j, x)

    def add_at(self, idx, increment):
        """
        Increment element at original index idx and update the BIT structure
        :param idx:           original index of the element to increment (BIT index = idx+1
        :param increment:   the value to increment
        :return:            updates the tree in place, returns None
        """
        bit_idx = idx + 1
        while bit_idx < len(self.tree_lst):
            self.tree_lst[bit_idx] += increment
            bit_idx += (bit_idx & -bit_idx)

    def prefix_sum(self, idx):
        """
        O(n*lg(n))  operations required
        :param j:   original index to calculate cumulative sum from 1 up to and including j
        :return:    the cumulative sum of the elements with indexes from 1 up to and including j,
                    AKA prefix sum
        """
        bit_idx = idx + 1
        pr_sum = 0
        while bit_idx:
            pr_sum += self.tree_lst[bit_idx]
            bit_idx -= (bit_idx & -bit_idx)
        return pr_sum

    def range_sum(self, i, j):
        """
        Cumulative sum of the elements between and including to the indexes i and j
        :param i:   the beginning index of the segment of elements to sum up
        :param j:   the last index of the segment of the elements to sum up
        :return:    the sum of the elements between and including to indices i and j
        """
        return self.prefix_sum(j) - self.prefix_sum(i - 1)

    def element(self, j):
        """
        Find and return the value of the element at BIT index j
        :param j:   element's index in the original list
        :return:    element(j)
        """
        return self.prefix_sum(j) - self.prefix_sum(j - 1)


if __name__ == "__main__":
    """
    Keeping some tests here as examples of the usage.
    Unit tests are also presented in the tests package.
    """


    def test_element():
        lst = [1, 5, 10, 100]
        bit = Bit(len(lst) + 1)
        bit.init_with_list(lst)
        elements = [bit.element(j) for j in range(len(lst))]
        # print(elements)
        assert lst == elements
        print('test_element passed')


    def test_range_sum():
        lst = [1, 5, 10, 100]
        bit = Bit(len(lst) + 1)
        bit.init_with_list(lst)
        expected_0_2 = 16
        realised = bit.range_sum(0, 2)
        # print(realised)
        assert expected_0_2 == realised
        print('test_range_sum passed')


    test_element()
    test_range_sum()
