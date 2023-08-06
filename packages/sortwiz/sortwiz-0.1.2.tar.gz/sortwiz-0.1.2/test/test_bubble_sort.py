import unittest

from sortwiz.errors import InvalidOrderError
from sortwiz.bubble_sort import BubbleSort
from sortwiz.base_sort import SortResult

class TestBubbleSort(unittest.TestCase):
    sut = BubbleSort()

    def test_items_type(self):
        # Arrange
        items = "any str"

        # Act & Assert
        with self.assertRaises(TypeError):
            self.sut.sort(items, True)

        with self.assertRaises(TypeError):
            self.sut.sort_asc(items, True)

        with self.assertRaises(TypeError):
            self.sut.sort_asc(items, True)

    def test_in_place_True_returns_same_list_reference(self):
        # Arrange
        in_place = True

        items = [5, 8, 2, 16, 0, -5]
        items_asc = list(items)
        items_desc = list(items)

        # Act
        result = self.sut.sort(items, in_place)
        result_asc = self.sut.sort_asc(items_asc, in_place)
        result_desc = self.sut.sort_desc(items_desc, in_place)

        # Assert
        self.assertEqual(items, result.value)
        self.assertEqual(items_asc, result_asc.value)
        self.assertEqual(items_desc, result_desc.value)

    def test_in_place_False_returns_different_list_reference(self):
        # Arrange
        in_place = False

        items = [5, 8, 2, 16, 0, -5]
        items_asc = list(items)
        items_desc = list(items)

        # Act
        result = self.sut.sort(items, in_place)
        result_asc = self.sut.sort_asc(items, in_place)
        result_desc = self.sut.sort_desc(items, in_place)

        # Assert
        self.assertNotEqual(items, result.value)
        self.assertNotEqual(items_asc, result_asc.value)
        self.assertNotEqual(items_desc, result_desc.value)
    
    def test_items_is_empty_returns_zero_for_swaps_and_writes(self):
        # Arrange
        empty_items = []

        # Act
        result = self.sut.sort(empty_items, True)

        # Assert
        self.assertEqual(0, result.swaps)
        self.assertEqual(0, result.writes)
        self.assertEqual(empty_items, result.value)

    def test_items_sort_asc(self):
        # Arrange
        items = [8, 5, 6, 1, 0, -10, 6]

        expected = list(items)
        expected.sort()

        # Act
        result = self.sut.sort(items, False)
        result_asc = self.sut.sort_asc(items, False)

        # Arrange
        self.assertListEqual(expected, result.value)
        self.assertListEqual(expected, result_asc.value)

    def test_items_sort_desc(self):
        # Arrange
        items = [8, 5, 6, 1, 0, -10, 6]

        expected = list(items)
        expected.sort(reverse=True)

        # Act
        result = self.sut.sort(items, False, True)
        result_desc = self.sut.sort_desc(items, False)

        # Arrange
        self.assertListEqual(expected, result.value)
        self.assertListEqual(expected, result_desc.value)

    def test_items_swaps_asc(self):
        # Arrange
        items = [4, 3, 1, 2]

        expected = 5

        # Act
        result = self.sut.sort(items, False)
        result_asc = self.sut.sort_asc(items, False)

        # Arrange
        self.assertEqual(expected, result.swaps)
        self.assertEqual(expected, result_asc.swaps)

    def test_items_swaps_desc(self):
        # Arrange
        items = [4, 3, 1, 2]

        expected = 1

        # Act
        result = self.sut.sort(items, False, True)
        result_desc = self.sut.sort_desc(items, False)

        # Arrange
        self.assertEqual(expected, result.swaps)
        self.assertEqual(expected, result_desc.swaps)

    def test_items_writes_asc(self):
        # Arrange
        items = [4, 3, 1, 2]

        expected = 10

        # Act
        result = self.sut.sort(items, False)
        result_asc = self.sut.sort_asc(items, False)

        # Arrange
        self.assertEqual(expected, result.writes)
        self.assertEqual(expected, result_asc.writes)

    def test_items_writes_desc(self):
        # Arrange
        items = [4, 3, 1, 2]

        expected = 2

        # Act
        result = self.sut.sort(items, False, True)
        result_desc = self.sut.sort_desc(items, False)

        # Arrange
        self.assertEqual(expected, result.writes)
        self.assertEqual(expected, result_desc.writes)
    
    def test_result_type(self):
        # Act
        result = self.sut.sort([], False)
        result_asc = self.sut.sort_asc([], False)
        result_desc = self.sut.sort_desc([], False)

        # Assert
        self.assertIsInstance(result, SortResult)
        self.assertIsInstance(result_asc, SortResult)
        self.assertIsInstance(result_desc, SortResult)
