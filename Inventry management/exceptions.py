"""
exceptions.py
-------------
Custom exception hierarchy for the inventory system.

Why custom exceptions instead of generic ones?
- They make error handling readable: `except InsufficientStockError` tells you exactly
  what went wrong, instead of catching a bare ValueError and guessing.
- They carry useful data (e.g. how much stock was available) that calling code can use.
"""


class InventoryError(Exception):
    """Base class for all inventory-related errors. Catch this to handle any of them generically."""


class ProductNotFoundError(InventoryError):
    def __init__(self, product_id):
        super().__init__(f"Product with ID '{product_id}' not found in inventory.")
        self.product_id = product_id


class DuplicateProductError(InventoryError):
    def __init__(self, product_id):
        super().__init__(f"Product with ID '{product_id}' already exists.")
        self.product_id = product_id


class InsufficientStockError(InventoryError):
    def __init__(self, product_id, requested, available):
        super().__init__(
            f"Cannot fulfill request for '{product_id}': requested {requested}, only {available} in stock."
        )
        self.product_id = product_id
        self.requested = requested
        self.available = available
