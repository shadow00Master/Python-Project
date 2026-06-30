"""
billing.py
----------
InvoiceItem represents one line on an invoice (a product + quantity sold).
Invoice ties multiple line items together, applies bulk discount + tax,
and prints a receipt.

Notice that Invoice never checks "if this is a ClearanceProduct, do X" —
it just calls product.get_unit_price() and lets polymorphism handle the
pricing differences. That's the whole point of designing it this way.
"""

from datetime import datetime

from inventory import Inventory
from exceptions import InsufficientStockError


class InvoiceItem:
    def __init__(self, product, quantity: int):
        self.product = product
        self.quantity = quantity

    @property
    def line_total(self) -> float:
        return round(self.product.get_unit_price() * self.quantity, 2)

    def __str__(self):
        return (f"{self.product.name:<28} x{self.quantity:<4} "
                f"@ Rs.{self.product.get_unit_price():>8.2f} = Rs.{self.line_total:>9.2f}")


class Invoice:
    BULK_DISCOUNT_THRESHOLD = 10   # total units across the invoice
    BULK_DISCOUNT_PERCENT = 5
    TAX_PERCENT = 5

    def __init__(self, customer_name: str, inventory: Inventory):
        self.customer_name = customer_name
        self.inventory = inventory
        self.items: list[InvoiceItem] = []
        self.created_at = datetime.now()

    def add_item(self, product_id: str, quantity: int):
        """Looks up the product, checks/reduces stock, and adds a line item.
        Raises ProductNotFoundError or InsufficientStockError if something's wrong —
        and importantly, stock is only reduced if the lookup succeeds."""
        product = self.inventory.get_product(product_id)
        if product.quantity < quantity:
            raise InsufficientStockError(product_id, quantity, product.quantity)
        self.inventory.reduce_stock(product_id, quantity)
        self.items.append(InvoiceItem(product, quantity))

    @property
    def subtotal(self) -> float:
        return round(sum(item.line_total for item in self.items), 2)

    @property
    def bulk_discount(self) -> float:
        total_units = sum(item.quantity for item in self.items)
        if total_units >= self.BULK_DISCOUNT_THRESHOLD:
            return round(self.subtotal * self.BULK_DISCOUNT_PERCENT / 100, 2)
        return 0.0

    @property
    def tax(self) -> float:
        return round((self.subtotal - self.bulk_discount) * self.TAX_PERCENT / 100, 2)

    @property
    def grand_total(self) -> float:
        return round(self.subtotal - self.bulk_discount + self.tax, 2)

    def build_receipt(self) -> str:
        lines = []
        lines.append("=" * 56)
        lines.append("INVOICE".center(56))
        lines.append("=" * 56)
        lines.append(f"Customer: {self.customer_name}")
        lines.append(f"Date:     {self.created_at.strftime('%Y-%m-%d %H:%M')}")
        lines.append("-" * 56)
        for item in self.items:
            lines.append(str(item))
        lines.append("-" * 56)
        lines.append(f"{'Subtotal:':<44}Rs.{self.subtotal:>9.2f}")
        if self.bulk_discount:
            lines.append(f"{'Bulk Discount:':<44}-Rs.{self.bulk_discount:>8.2f}")
        lines.append(f"{'Tax (' + str(self.TAX_PERCENT) + '%):':<44}Rs.{self.tax:>9.2f}")
        lines.append(f"{'GRAND TOTAL:':<44}Rs.{self.grand_total:>9.2f}")
        lines.append("=" * 56)
        return "\n".join(lines)

    def print_receipt(self):
        receipt = self.build_receipt()
        print(receipt)
        return receipt
