"""
main.py
-------
CLI entry point. Run with: python main.py

This is intentionally a plain text menu — no extra dependencies needed.
Once you're comfortable with this, the natural next step is wrapping
Inventory/Invoice in a Flask app with REST endpoints.
"""

from inventory import Inventory
from billing import Invoice
from models import TextileProduct, ClearanceProduct, ImportedProduct
from exceptions import InventoryError


def seed_sample_data(inventory: Inventory):
    """Adds a few sample products on first run, so the demo isn't empty."""
    if inventory.list_products():
        return
    sample_products = [
        TextileProduct("BS001", "Cotton Bedsheet (King)", 1800, 25, fabric="Cotton"),
        TextileProduct("PL001", "Microfiber Pillow", 650, 40),
        ClearanceProduct("BL001", "Winter Blanket - Last Season", 2200, 10, discount_percent=30),
        ImportedProduct("MP001", "Imported Mattress Protector", 3200, 15, import_duty_percent=12),
    ]
    for p in sample_products:
        inventory.add_product(p)


def print_menu():
    print("""
--- Inventory & Billing System ---
1. View all products
2. Search product
3. Add new product
4. Restock product
5. View low stock report
6. Create new invoice
7. View total inventory value
0. Exit
""")


def handle_view_all(inventory):
    products = inventory.list_products()
    if not products:
        print("No products in inventory.")
        return
    for p in products:
        print(p)


def handle_search(inventory):
    keyword = input("Search keyword: ").strip()
    results = inventory.search(keyword)
    if not results:
        print("No matching products found.")
    for p in results:
        print(p)


def handle_add_product(inventory):
    print("Product type: 1) Textile  2) Clearance  3) Imported")
    choice = input("Choose type: ").strip()
    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()

    try:
        price = float(input("Price: ").strip())
        quantity = int(input("Quantity: ").strip())

        if choice == "1":
            product = TextileProduct(product_id, name, price, quantity)
        elif choice == "2":
            discount = float(input("Discount %: ").strip())
            product = ClearanceProduct(product_id, name, price, quantity, discount_percent=discount)
        elif choice == "3":
            duty = float(input("Import duty %: ").strip())
            product = ImportedProduct(product_id, name, price, quantity, import_duty_percent=duty)
        else:
            print("Invalid product type.")
            return

        inventory.add_product(product)
        print(f"Added: {product}")
    except InventoryError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Invalid input: {e}")


def handle_restock(inventory):
    product_id = input("Product ID: ").strip()
    try:
        amount = int(input("Restock amount: ").strip())
        inventory.restock(product_id, amount)
        print("Restocked successfully.")
    except InventoryError as e:
        print(f"Error: {e}")
    except ValueError:
        print("Amount must be a number.")


def handle_low_stock(inventory):
    raw = input("Low stock threshold (default 5): ").strip()
    threshold = int(raw) if raw else 5
    items = inventory.low_stock_report(threshold)
    if not items:
        print("No products below threshold.")
    for p in items:
        print(f"LOW STOCK: {p}")


def handle_create_invoice(inventory):
    customer = input("Customer name: ").strip()
    invoice = Invoice(customer, inventory)
    while True:
        product_id = input("Product ID to add (or 'done'): ").strip()
        if product_id.lower() == "done":
            break
        try:
            quantity = int(input("Quantity: ").strip())
            invoice.add_item(product_id, quantity)
            print("Added to invoice.")
        except InventoryError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Quantity must be a number.")

    if invoice.items:
        invoice.print_receipt()
    else:
        print("Invoice cancelled - no items added.")


def main():
    inventory = Inventory()
    seed_sample_data(inventory)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            handle_view_all(inventory)
        elif choice == "2":
            handle_search(inventory)
        elif choice == "3":
            handle_add_product(inventory)
        elif choice == "4":
            handle_restock(inventory)
        elif choice == "5":
            handle_low_stock(inventory)
        elif choice == "6":
            handle_create_invoice(inventory)
        elif choice == "7":
            print(f"Total inventory value: Rs.{inventory.total_inventory_value():.2f}")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
