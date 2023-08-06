from datetime import timedelta

class SortResult:
    def __init__(self, value: list, swaps: int, writes: int, time: timedelta):
        self.value = value
        self.swaps = swaps
        self.writes = writes
        self.time = time

    def __str__(self) -> str:
        return f'''
Sort result
| value (first 10) - {self.value[:10]}
| swaps - {self.swaps}
| writes - {self.writes}
| time - {self.time}
'''

class BaseSort:
    @classmethod
    def sort_asc(self, items: list, in_place: bool = False) -> SortResult:
        raise NotImplementedError()
    
    @classmethod
    def sort_desc(self, items: list, in_place: bool = False) -> SortResult:
        raise NotImplementedError()
    
    @classmethod
    def sort(self, items: list, in_place: bool = False, reverse: bool = False) -> SortResult:
        raise NotImplementedError()
    
    @staticmethod
    def validate(items) -> None:
        '''
        Validates if `items` is of type list.

        Returns
        -------
            `None`.

        Raises
        ------
            `TypeError` if items isn't a list.
        '''
        
        items_type = type(items)
        if items_type != list:
            raise TypeError(f"Parameter 'items' expected be a list. Given: {items_type}.")
    
    @staticmethod
    def swap(items: list, i: int, j: int, sorting_result: SortResult) -> None:
        items[i], items[j] = items[j], items[i]
        sorting_result.writes += 2
        sorting_result.swaps += 1
