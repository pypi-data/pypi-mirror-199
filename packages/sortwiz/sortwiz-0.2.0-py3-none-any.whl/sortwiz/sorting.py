from .base_sort import SortResult
from .bubble_sort import BubbleSort
from .quicksort import Quicksort

class SortWizard:
    __bubble_sort = BubbleSort()
    __quicksort = Quicksort()

    @staticmethod
    def bubble_sort(items: list, in_place : bool = False, reverse: bool = False) -> SortResult:
        '''
        Applies a bubble sort to `items`.

        Parameters
        ----------
            `items` - A list with items to sort.
            `in_place` - Whether to apply the sort into the given list or not. If True, modifies the given list, if False, not.
            `reverse` - `True` for descending, `False` for ascending.

        Returns
        -------
            The `SortResult` with the list of items.
        '''

        return SortWizard.__bubble_sort.sort(items, in_place, reverse)
    
    @staticmethod
    def quicksort(items: list, in_place : bool = False, reverse: bool = False) -> SortResult:
        '''
        Applies a quicksort to `items`.

        Parameters
        ----------
            `items` - A list with items to sort.
            `in_place` - Whether to apply the sort into the given list or not. If True, modifies the given list, if False, not.
            `reverse` - `True` for descending, `False` for ascending.

        Returns
        -------
            The `SortResult` with the list of items.
        '''

        return SortWizard.__quicksort.sort(items, in_place, reverse)
    