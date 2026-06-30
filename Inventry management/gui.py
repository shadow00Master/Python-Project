"""
gui.py
------
Tkinter desktop GUI for the Inventory & Billing System.
Run with: python gui.py

This reuses the exact same Inventory / Invoice / Product classes as main.py
(the CLI version) — the GUI is just a different "view" on top of the same
business logic. That separation (UI layer vs. logic layer) is itself a good
thing to be able to talk about in an interview.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from inventory import Inventory
from billing import Invoice
from models import TextileProduct, ClearanceProduct, ImportedProduct
from exceptions import InventoryError


PRODUCT_TYPES = {
    "Textile": TextileProduct,
    "Clearance": ClearanceProduct,
    "Imported": ImportedProduct,
}


def seed_sample_data(inventory: Inventory):
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


class InventoryApp(tk.Tk):
    """Main application window. Holds one Inventory instance shared across all tabs."""

    def __init__(self):
        super().__init__()
        self.title("Inventory & Billing System")
        self.geometry("900x560")
        self.minsize(800, 500)

        self.inventory = Inventory()
        seed_sample_data(self.inventory)

        self.cart_items = []  # list of (product_id, name, quantity) for the current invoice

        self._build_layout()
        self.refresh_inventory_view()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_layout(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.inventory_tab = ttk.Frame(notebook)
        self.add_product_tab = ttk.Frame(notebook)
        self.billing_tab = ttk.Frame(notebook)
        self.reports_tab = ttk.Frame(notebook)

        notebook.add(self.inventory_tab, text="Inventory")
        notebook.add(self.add_product_tab, text="Add Product")
        notebook.add(self.billing_tab, text="Create Invoice")
        notebook.add(self.reports_tab, text="Reports")

        self._build_inventory_tab()
        self._build_add_product_tab()
        self._build_billing_tab()
        self._build_reports_tab()

    # ------------------------------------------------------------------
    # Tab 1: Inventory
    # ------------------------------------------------------------------
    def _build_inventory_tab(self):
        frame = self.inventory_tab

        search_frame = ttk.Frame(frame)
        search_frame.pack(fill="x", padx=10, pady=(10, 5))
        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_inventory_view())
        ttk.Button(search_frame, text="Clear", command=self._clear_search).pack(side="left")

        columns = ("id", "name", "category", "unit_price", "quantity", "total_value")
        headings = {
            "id": "Product ID", "name": "Name", "category": "Category",
            "unit_price": "Unit Price", "quantity": "Qty", "total_value": "Stock Value",
        }
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        action_frame = ttk.Frame(frame)
        action_frame.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Label(action_frame, text="Restock amount:").pack(side="left")
        self.restock_amount_var = tk.StringVar()
        ttk.Entry(action_frame, textvariable=self.restock_amount_var, width=8).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Restock Selected", command=self._restock_selected).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Remove Selected", command=self._remove_selected).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Refresh", command=self.refresh_inventory_view).pack(side="right")

    def _clear_search(self):
        self.search_var.set("")
        self.refresh_inventory_view()

    def _get_selected_product_id(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a product first.")
            return None
        return self.tree.item(selection[0], "values")[0]

    def _restock_selected(self):
        product_id = self._get_selected_product_id()
        if not product_id:
            return
        amount_str = self.restock_amount_var.get().strip()
        if not amount_str.isdigit():
            messagebox.showerror("Invalid amount", "Restock amount must be a positive whole number.")
            return
        try:
            self.inventory.restock(product_id, int(amount_str))
            self.restock_amount_var.set("")
            self.refresh_inventory_view()
            messagebox.showinfo("Success", f"Restocked {product_id} by {amount_str} units.")
        except InventoryError as e:
            messagebox.showerror("Error", str(e))

    def _remove_selected(self):
        product_id = self._get_selected_product_id()
        if not product_id:
            return
        if not messagebox.askyesno("Confirm removal", f"Remove product '{product_id}' from inventory?"):
            return
        try:
            self.inventory.remove_product(product_id)
            self.refresh_inventory_view()
        except InventoryError as e:
            messagebox.showerror("Error", str(e))

    def refresh_inventory_view(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        keyword = self.search_var.get().strip() if hasattr(self, "search_var") else ""
        products = self.inventory.search(keyword) if keyword else self.inventory.list_products()

        for p in products:
            self.tree.insert("", "end", values=(
                p.product_id, p.name, p.category(),
                f"Rs.{p.get_unit_price():.2f}", p.quantity, f"Rs.{p.total_value():.2f}",
            ))

        # Keep other tabs in sync (product dropdown for billing, totals for reports)
        if hasattr(self, "billing_product_combo"):
            self._refresh_billing_product_list()
        if hasattr(self, "total_value_label"):
            self._refresh_reports_tab()

    # ------------------------------------------------------------------
    # Tab 2: Add Product
    # ------------------------------------------------------------------
    def _build_add_product_tab(self):
        frame = self.add_product_tab
        form = ttk.Frame(frame)
        form.pack(padx=20, pady=20, anchor="n")

        ttk.Label(form, text="Product Type:").grid(row=0, column=0, sticky="w", pady=6)
        self.new_type_var = tk.StringVar(value="Textile")
        type_combo = ttk.Combobox(form, textvariable=self.new_type_var, values=list(PRODUCT_TYPES.keys()),
                                   state="readonly", width=20)
        type_combo.grid(row=0, column=1, pady=6, sticky="w")
        type_combo.bind("<<ComboboxSelected>>", lambda e: self._update_extra_field_label())

        ttk.Label(form, text="Product ID:").grid(row=1, column=0, sticky="w", pady=6)
        self.new_id_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.new_id_var, width=30).grid(row=1, column=1, pady=6, sticky="w")

        ttk.Label(form, text="Name:").grid(row=2, column=0, sticky="w", pady=6)
        self.new_name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.new_name_var, width=30).grid(row=2, column=1, pady=6, sticky="w")

        ttk.Label(form, text="Price (Rs.):").grid(row=3, column=0, sticky="w", pady=6)
        self.new_price_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.new_price_var, width=30).grid(row=3, column=1, pady=6, sticky="w")

        ttk.Label(form, text="Quantity:").grid(row=4, column=0, sticky="w", pady=6)
        self.new_qty_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.new_qty_var, width=30).grid(row=4, column=1, pady=6, sticky="w")

        self.extra_field_label = ttk.Label(form, text="Fabric:")
        self.extra_field_label.grid(row=5, column=0, sticky="w", pady=6)
        self.new_extra_var = tk.StringVar(value="Cotton")
        self.extra_field_entry = ttk.Entry(form, textvariable=self.new_extra_var, width=30)
        self.extra_field_entry.grid(row=5, column=1, pady=6, sticky="w")

        ttk.Button(form, text="Add Product", command=self._add_product).grid(
            row=6, column=0, columnspan=2, pady=16)

        self.add_status_label = ttk.Label(form, text="", foreground="green")
        self.add_status_label.grid(row=7, column=0, columnspan=2)

    def _update_extra_field_label(self):
        product_type = self.new_type_var.get()
        if product_type == "Textile":
            self.extra_field_label.config(text="Fabric:")
            self.new_extra_var.set("Cotton")
        elif product_type == "Clearance":
            self.extra_field_label.config(text="Discount %:")
            self.new_extra_var.set("20")
        elif product_type == "Imported":
            self.extra_field_label.config(text="Import Duty %:")
            self.new_extra_var.set("10")

    def _add_product(self):
        product_type = self.new_type_var.get()
        product_id = self.new_id_var.get().strip()
        name = self.new_name_var.get().strip()

        if not product_id or not name:
            messagebox.showerror("Missing fields", "Product ID and Name are required.")
            return
        try:
            price = float(self.new_price_var.get().strip())
            quantity = int(self.new_qty_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid input", "Price must be a number and Quantity must be a whole number.")
            return

        try:
            if product_type == "Textile":
                product = TextileProduct(product_id, name, price, quantity, fabric=self.new_extra_var.get())
            elif product_type == "Clearance":
                discount = float(self.new_extra_var.get())
                product = ClearanceProduct(product_id, name, price, quantity, discount_percent=discount)
            else:  # Imported
                duty = float(self.new_extra_var.get())
                product = ImportedProduct(product_id, name, price, quantity, import_duty_percent=duty)

            self.inventory.add_product(product)
            self.add_status_label.config(text=f"Added '{name}' successfully.", foreground="green")

            # Clear form for the next entry
            self.new_id_var.set("")
            self.new_name_var.set("")
            self.new_price_var.set("")
            self.new_qty_var.set("")
            self.refresh_inventory_view()
        except InventoryError as e:
            messagebox.showerror("Error", str(e))
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))

    # ------------------------------------------------------------------
    # Tab 3: Create Invoice
    # ------------------------------------------------------------------
    def _build_billing_tab(self):
        frame = self.billing_tab

        top = ttk.Frame(frame)
        top.pack(fill="x", padx=15, pady=10)
        ttk.Label(top, text="Customer Name:").pack(side="left")
        self.customer_name_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.customer_name_var, width=30).pack(side="left", padx=8)

        add_row = ttk.Frame(frame)
        add_row.pack(fill="x", padx=15, pady=5)
        ttk.Label(add_row, text="Product:").pack(side="left")
        self.billing_product_var = tk.StringVar()
        self.billing_product_combo = ttk.Combobox(add_row, textvariable=self.billing_product_var,
                                                    state="readonly", width=40)
        self.billing_product_combo.pack(side="left", padx=8)
        ttk.Label(add_row, text="Qty:").pack(side="left")
        self.billing_qty_var = tk.StringVar(value="1")
        ttk.Entry(add_row, textvariable=self.billing_qty_var, width=6).pack(side="left", padx=8)
        ttk.Button(add_row, text="Add to Cart", command=self._add_to_cart).pack(side="left", padx=8)

        cart_columns = ("name", "quantity", "unit_price", "line_total")
        cart_headings = {"name": "Product", "quantity": "Qty", "unit_price": "Unit Price", "line_total": "Line Total"}
        self.cart_tree = ttk.Treeview(frame, columns=cart_columns, show="headings", height=8)
        for col in cart_columns:
            self.cart_tree.heading(col, text=cart_headings[col])
            self.cart_tree.column(col, width=150, anchor="center")
        self.cart_tree.column("name", width=220, anchor="w")
        self.cart_tree.pack(fill="both", expand=True, padx=15, pady=10)

        bottom = ttk.Frame(frame)
        bottom.pack(fill="x", padx=15, pady=(0, 10))
        ttk.Button(bottom, text="Remove Selected Line", command=self._remove_cart_line).pack(side="left")
        ttk.Button(bottom, text="Clear Cart", command=self._clear_cart).pack(side="left", padx=8)
        ttk.Button(bottom, text="Generate Invoice", command=self._generate_invoice).pack(side="right")

    def _refresh_billing_product_list(self):
        products = self.inventory.list_products()
        labels = [f"{p.product_id} - {p.name} ({p.quantity} in stock)" for p in products]
        self.billing_product_combo["values"] = labels
        if labels and not self.billing_product_var.get():
            self.billing_product_combo.current(0)

    def _add_to_cart(self):
        selected = self.billing_product_var.get()
        if not selected:
            messagebox.showwarning("No product", "Please select a product.")
            return
        product_id = selected.split(" - ")[0]

        qty_str = self.billing_qty_var.get().strip()
        if not qty_str.isdigit() or int(qty_str) <= 0:
            messagebox.showerror("Invalid quantity", "Quantity must be a positive whole number.")
            return
        quantity = int(qty_str)

        try:
            product = self.inventory.get_product(product_id)
        except InventoryError as e:
            messagebox.showerror("Error", str(e))
            return

        # Check against remaining stock minus what's already reserved in the cart for this product
        already_in_cart = sum(q for pid, _, q in self.cart_items if pid == product_id)
        if product.quantity - already_in_cart < quantity:
            messagebox.showerror(
                "Insufficient stock",
                f"Only {product.quantity - already_in_cart} unit(s) of '{product.name}' available."
            )
            return

        self.cart_items.append((product_id, product.name, quantity))
        self._refresh_cart_view()

    def _refresh_cart_view(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        for product_id, name, quantity in self.cart_items:
            product = self.inventory.get_product(product_id)
            unit_price = product.get_unit_price()
            line_total = round(unit_price * quantity, 2)
            self.cart_tree.insert("", "end", values=(name, quantity, f"Rs.{unit_price:.2f}", f"Rs.{line_total:.2f}"))

    def _remove_cart_line(self):
        selection = self.cart_tree.selection()
        if not selection:
            return
        index = self.cart_tree.index(selection[0])
        del self.cart_items[index]
        self._refresh_cart_view()

    def _clear_cart(self):
        self.cart_items = []
        self._refresh_cart_view()

    def _generate_invoice(self):
        customer = self.customer_name_var.get().strip()
        if not customer:
            messagebox.showerror("Missing customer", "Please enter a customer name.")
            return
        if not self.cart_items:
            messagebox.showwarning("Empty cart", "Add at least one product to the cart first.")
            return

        invoice = Invoice(customer, self.inventory)
        try:
            for product_id, _, quantity in self.cart_items:
                invoice.add_item(product_id, quantity)
        except InventoryError as e:
            messagebox.showerror("Error", str(e))
            self.refresh_inventory_view()
            return

        self._show_receipt_window(invoice.build_receipt())

        # Reset the billing tab for the next customer
        self.customer_name_var.set("")
        self.cart_items = []
        self._refresh_cart_view()
        self.refresh_inventory_view()

    def _show_receipt_window(self, receipt_text):
        win = tk.Toplevel(self)
        win.title("Invoice Receipt")
        win.geometry("560x440")
        win.resizable(False, False)

        text_widget = tk.Text(win, font=("Courier New", 10), wrap="none", padx=8, pady=8)
        text_widget.insert("1.0", receipt_text)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 10))

    # ------------------------------------------------------------------
    # Tab 4: Reports
    # ------------------------------------------------------------------
    def _build_reports_tab(self):
        frame = self.reports_tab

        value_frame = ttk.Frame(frame)
        value_frame.pack(fill="x", padx=15, pady=15)
        ttk.Label(value_frame, text="Total Inventory Value:", font=("Segoe UI", 11, "bold")).pack(side="left")
        self.total_value_label = ttk.Label(value_frame, text="Rs.0.00", font=("Segoe UI", 11))
        self.total_value_label.pack(side="left", padx=10)

        threshold_frame = ttk.Frame(frame)
        threshold_frame.pack(fill="x", padx=15, pady=5)
        ttk.Label(threshold_frame, text="Low stock threshold:").pack(side="left")
        self.threshold_var = tk.StringVar(value="5")
        ttk.Entry(threshold_frame, textvariable=self.threshold_var, width=6).pack(side="left", padx=8)
        ttk.Button(threshold_frame, text="Check Low Stock", command=self._refresh_reports_tab).pack(side="left")

        columns = ("id", "name", "quantity")
        self.low_stock_tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        self.low_stock_tree.heading("id", text="Product ID")
        self.low_stock_tree.heading("name", text="Name")
        self.low_stock_tree.heading("quantity", text="Qty Remaining")
        self.low_stock_tree.column("name", width=250, anchor="w")
        self.low_stock_tree.pack(fill="both", expand=True, padx=15, pady=10)

    def _refresh_reports_tab(self):
        self.total_value_label.config(text=f"Rs.{self.inventory.total_inventory_value():.2f}")

        for row in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(row)

        threshold_str = self.threshold_var.get().strip() if hasattr(self, "threshold_var") else "5"
        threshold = int(threshold_str) if threshold_str.isdigit() else 5

        for p in self.inventory.low_stock_report(threshold):
            self.low_stock_tree.insert("", "end", values=(p.product_id, p.name, p.quantity))


if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
