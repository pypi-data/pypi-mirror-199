class InvalidOrderError(Exception):
    def __init__(self, order) -> None:
        self.order = order
        self.message = f"Invalid sorting order given: {self.order}.\nUse SortingWizard.ASCENDING and SortingWizard.DESCENDING for valid orders."
        super().__init__(self.message)
        