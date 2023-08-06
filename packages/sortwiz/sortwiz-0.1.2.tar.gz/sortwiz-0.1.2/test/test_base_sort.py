import unittest

from sortwiz.base_sort import BaseSort, SortResult

class TestBaseSort(unittest.TestCase):
    sut = BaseSort()

    def test_validate(self):
        # Arrange
        items = "any str"

        # Act & Assert
        with self.assertRaises(TypeError):
            self.sut.validate(items)

    def test_sort_not_implemented(self):
         # Act & Assert
        with self.assertRaises(NotImplementedError):
            self.sut.sort([], True, 1)

        with self.assertRaises(NotImplementedError):
            self.sut.sort_asc([], True)

        with self.assertRaises(NotImplementedError):
            self.sut.sort_asc([], True)

    def test_swap(self):
        # Arrange
        items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        item_to_be_swapped = 998
        item_to_be_swapped_index = 0
        another_item_to_be_swapped = 999
        another_item_to_be_swapped_index = 3

        items[item_to_be_swapped_index] = item_to_be_swapped
        items[another_item_to_be_swapped_index] = another_item_to_be_swapped

        sort_result = SortResult([], 0, 0, 0)

        # Act
        BaseSort.swap(items, item_to_be_swapped_index, another_item_to_be_swapped_index, sort_result)

        # Assert
        self.assertEqual(item_to_be_swapped, items[another_item_to_be_swapped_index])
        self.assertEqual(another_item_to_be_swapped, items[item_to_be_swapped_index])


    