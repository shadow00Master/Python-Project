"""
inventory.py
------------
The Inventory class owns the collection of products and all stock operations.
It also handles saving/loading to a JSON file so data survives between runs.
"""

import json
from pathlib import Path

from models import Product, TextileProduct, ClearanceProduct, ImportedProduct
from exceptions import ProductNotFoundError, InsufficientStockError, DuplicateProductError

# Maps the string saved in JSON ("type") back to the actual class, so we can
# reconstruct the right kind of Product object when loading from disk.
PRODUCT_CLASSES = {
    "TextileProduct": TextileProduct,
    "ClearanceProduct": ClearanceProduct,
    "ImportedProduct": ImportedProduct,
}


class Inventory:
    def __init__(self, data_file="inventory_data.json"):
        self._products: dict[str, Product] = {}
        self._data_file = Path(data_file)
        self.load()

    # ---- Core operations ----
    def add_product(self, product: Product):
        if product.product_id in self._products:
            raise DuplicateProductError(product.product_id)
        self._products[product.product_id] = product
        self.save()

    def get_product(self, product_id: str) -> Product:
        if product_id not in self._products:
            raise ProductNotFoundError(product_id)
        return self._products[product_id]

    def remove_product(self, product_id: str):
        self.get_product(product_id)  # raises ProductNotFoundError if missing
        del self._products[product_id]
        self.save()

    def restock(self, product_id: str, amount: int):
        product = self.get_product(product_id)
        product.quantity += amount
        self.save()

    def reduce_stock(self, product_id: str, amount: int):
        product = self.get_product(product_id)
        if product.quantity < amount:
            raise InsufficientStockError(product_id, amount, product.quantity)
        product.quantity -= amount
        self.save()

    def list_products(self):
        return list(self._products.values())

    def low_stock_report(self, threshold: int = 5):
        return [p for p in self._products.values() if p.quantity <= threshold]

    def total_inventory_value(self) -> float:
        return round(sum(p.total_value() for p in self._products.values()), 2)

    def search(self, keyword: str):
        keyword = keyword.lower()
        return [p for p in self._products.values() if keyword in p.name.lower()]

    # ---- Persistence ----
    def save(self):
        data = [p.to_dict() for p in self._products.values()]
        with open(self._data_file, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not self._data_file.exists():
            return
        with open(self._data_file, "r") as f:
            data = json.load(f)
        for item in data:
            item = dict(item)  # don't mutate the loaded dict in place
            cls = PRODUCT_CLASSES.get(item.pop("type", None))
            if cls:
                product = cls(**item)
                self._products[product.product_id] = product
