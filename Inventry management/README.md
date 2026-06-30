# Inventory & Billing System

A command-line inventory and billing system, built to demonstrate all four
pillars of Object-Oriented Programming with realistic business logic
(stock validation, tiered pricing, bulk discounts, tax, invoicing).

## How to run

```bash
python main.py
```

No external dependencies — pure Python standard library. First run seeds
4 sample products automatically. Data is saved to `inventory_data.json`
so your stock persists between runs.

## Project structure

```
models.py      -> Product class hierarchy
exceptions.py  -> Custom exceptions (ProductNotFoundError, InsufficientStockError, ...)
inventory.py   -> Inventory class: stock operations + JSON persistence
billing.py     -> InvoiceItem & Invoice classes: pricing, discounts, tax, receipts
main.py        -> CLI menu that ties everything together
```

## OOP concepts used (and where to find them)

| Concept | Where |
|---|---|
| **Abstraction** | `Product` is an `ABC` — `get_unit_price()` and `category()` are abstract methods every subclass must implement |
| **Encapsulation** | `price` and `quantity` are private (`_price`, `_quantity`) and only modified through validated property setters — you can't set a negative price or quantity |
| **Inheritance** | `TextileProduct`, `ClearanceProduct`, `ImportedProduct` all inherit shared behavior (`total_value()`, `to_dict()`, `__str__`) from `Product` |
| **Polymorphism** | `Invoice` and `Inventory` call `product.get_unit_price()` without ever checking *which* subclass they have — each class calculates its own price differently (clearance discount vs. import duty vs. plain price) |

## Business rules implemented

- Each product type prices itself differently (this is the polymorphism in action)
- Stock can never go negative — adding an invoice item that exceeds available stock raises `InsufficientStockError` *before* anything is deducted
- Orders totaling 10+ units get a 5% bulk discount on the invoice
- 5% sales tax applied after the discount
- Low-stock report flags anything at or below a threshold you choose

## Ideas to extend this for your portfolio

1. **Add a Flask REST API** on top of `Inventory`/`Invoice` (`POST /products`, `POST /invoices`, etc.) — natural next step if you're already learning Flask
2. **Swap JSON for SQLite/PostgreSQL** — same `Inventory` interface, just change `save()`/`load()`
3. **Add a `PerishableProduct`** with an expiry date that triggers automatic markdown as it nears expiry
4. **Export invoices to PDF** instead of just printing to console
5. **Add user roles** (admin vs. cashier) with different permissions — good excuse to demo a `User` class hierarchy too

## Why this is a good portfolio project

It's not a toy "Animal/Dog/Cat" example — it models a real problem (a small
shop tracking stock and billing customers) with rules that actually matter:
stock can't go negative, discounts apply correctly, pricing logic is cleanly
separated by product type. That's exactly the kind of design judgment
interviewers are trying to assess when they ask OOP questions.
