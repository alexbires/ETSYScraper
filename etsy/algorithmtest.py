import unittest
from algorithm import Algorithm as alg
from listing import Listing as lis
from words import ShopAndWords as shop


class AlgorithmTest(unittest.TestCase):
    """
    Ensures that the algorithm is working properly
    """

    def test_basic_output(self):
        """Ensures that the lowest frequency words are going to be picked"""
        etsy1 = lis(
            "ab ab ab ab ac ac ac aa z q w e t amazing",
            "this a desc desc this other of amazing objects with other\
            objects between between",
            1)

        alg_test = alg([etsy1], 1)
        should_be = shop(1, None, ["q", "w", "e", "t", "z"], None)
        returned = alg_test.process_data()

        # sort is there becase we don't care about the order of the list
        # we just care about that the contents are the same
        self.assertEqual(returned.words_list.sort(),
                         should_be.words_list.sort())


if __name__ == "__main__":
    unittest.main()
