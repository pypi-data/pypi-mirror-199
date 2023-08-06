from datetime import datetime

from .base_sort import BaseSort, SortResult

class BubbleSort(BaseSort):
    @classmethod
    def sort_asc(self, items: list, in_place: bool = False) -> SortResult:
        '''
        Applies a bubble sort in ascending order to `items`.

        Parameters
        ----------
            `items` - A list with items to sort.
            `in_place` - Whether to apply the sort into the given list or not. If True, modifies the given list, if False, not.

        Returns
        -------
            The `SortResult` with the list of items in ascending order.
        '''

        return self.sort(items, in_place, False)
    
    @classmethod
    def sort_desc(self, items: list, in_place: bool = False) -> SortResult:
        '''
        Applies a bubble sort in descending order to `items`.

        Parameters
        ----------
            `items` - A list with items to sort.
            `in_place` - Whether to apply the sort into the given list or not. If True, modifies the given list, if False, not.

        Returns
        -------
            The `SortResult` with the list of items in descending order.
        '''

        return self.sort(items, in_place, True)
    
    @classmethod
    def sort(self, items: list, in_place: bool = False, reverse: bool = False) -> SortResult:
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
        
        self.validate(items)

        start_time = datetime.now()

        swapped = True
        sorted_list = items if in_place else list(items)
        sort_result = SortResult(sorted_list, 0, 0, 0)

        while swapped:
            swapped = False

            for i in range(len(sorted_list) - 1):
                if sorted_list[i] > sorted_list[i + 1]:
                    self.swap(sorted_list, i, i + 1, sort_result)
                    swapped = True

        end_time = datetime.now()

        sort_result.time = end_time - start_time

        if reverse:
            BaseSort.reverse(sort_result.value)

        return sort_result
