from .base_sort import SortResult
from .bubble_sort import BubbleSort

class SortWizard:
    _bubble_sort = BubbleSort()

    @staticmethod
    def bubble_sort(items: list, in_place : bool = False, reverse: bool = False) -> SortResult:
        '''
        Applies a bubble sort to the given list.

        Parameters
        ----------
            `items` - A list with items to sort.
            `in_place` - Whether to apply the sort into the given list or not. If True, modifies the given list, if False, not.
            `reverse` - `True` for descending, `False` for ascending.

        Returns
        -------
            The `SortResult` with the list of items.
        '''

        return SortWizard._bubble_sort.sort(items, in_place, reverse)
    