"""
models.py
---------
Defines the Product class hierarchy.

OOP concepts demonstrated:
- Abstraction:    Product is an ABC; subclasses must implement get_unit_price() and category()
- Encapsulation:  price/quantity are private attrs accessed via validated properties
- Inheritance:    TextileProduct, ClearanceProduct, ImportedProduct all extend Product
- Polymorphism:   each subclass calculates get_unit_price() differently, but callers
                  (Inventory, Invoice) just call product.get_unit_price() without caring which type it is
"""

from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class for anything that can be stocked and sold."""

    def __init__(self, product_id: str, name: str, price: float, quantity: int):
        self._product_id = product_id
        self._name = name
        self._price = self._validate_price(price)
        self._quantity = self._validate_quantity(quantity)

    # ---- Encapsulation: validated access to internal state ----
    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value):
        self._price = self._validate_price(value)

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = self._validate_quantity(value)

    @staticmethod
    def _validate_price(price) -> float:
        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price

    @staticmethod
    def _validate_quantity(quantity) -> int:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        return quantity

    # ---- Abstraction: every product type must define these ----
    @abstractmethod
    def get_unit_price(self) -> float:
        """Effective selling price per unit (after any product-specific pricing rule)."""
        raise NotImplementedError

    @abstractmethod
    def category(self) -> str:
        raise NotImplementedError

    # ---- Shared behaviour, inherited by all subclasses ----
    def total_value(self) -> float:
        """Total stock value at current selling price."""
        return round(self.get_unit_price() * self._quantity, 2)

    def to_dict(self) -> dict:
        """Used for JSON persistence."""
        return {
            "type": self.__class__.__name__,
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity": self._quantity,
        }

    def __str__(self):
        return (f"[{self.category()}] {self._name} (ID: {self._product_id}) "
                f"- Rs.{self.get_unit_price():.2f} x {self._quantity} in stock")


class TextileProduct(Product):
    """Everyday catalog item — bedsheets, pillows, towels. No special pricing rule."""

    def __init__(self, product_id, name, price, quantity, fabric="Cotton"):
        super().__init__(product_id, name, price, quantity)
        self.fabric = fabric

    def get_unit_price(self) -> float:
        return self._price

    def category(self) -> str:
        return "Textile"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["fabric"] = self.fabric
        return data


class ClearanceProduct(Product):
    """End-of-season stock — automatically discounted off the base price."""

    def __init__(self, product_id, name, price, quantity, discount_percent=20):
        super().__init__(product_id, name, price, quantity)
        self.discount_percent = discount_percent

    def get_unit_price(self) -> float:
        return round(self._price * (1 - self.discount_percent / 100), 2)

    def category(self) -> str:
        return "Clearance"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["discount_percent"] = self.discount_percent
        return data


class ImportedProduct(Product):
    """Imported items — import duty adds on top of the base price."""

    def __init__(self, product_id, name, price, quantity, import_duty_percent=10):
        super().__init__(product_id, name, price, quantity)
        self.import_duty_percent = import_duty_percent

    def get_unit_price(self) -> float:
        return round(self._price * (1 + self.import_duty_percent / 100), 2)

    def category(self) -> str:
        return "Imported"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["import_duty_percent"] = self.import_duty_percent
        return data
