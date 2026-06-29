# Library Management System

A command-line library management system built in pure Python (no external
libraries) to demonstrate core object-oriented programming concepts.

## What it does

- Add books and magazines to a catalog
- Register members
- Borrow and return items, with due dates and overdue tracking
- Saves all data to `library_data.json` so it persists between runs

## How to run

```
python main.py
```

Follow the on-screen numbered menu.

## OOP concepts this demonstrates

- **Inheritance**: `Book` and `Magazine` both inherit from a shared
  `LibraryItem` base class (borrow/return logic is written once).
- **Polymorphism**: `Magazine` overrides `LOAN_DAYS` and `__str__()` to behave
  differently from `Book` while using the same interface.
- **Encapsulation**: `is_borrowed` is exposed as a read-only property; the
  internal `_is_borrowed` flag can only change through `borrow()` /
  `return_item()`, so the object's state can't be corrupted from outside.
- **Composition**: `Library` is made up of `LibraryItem` and `Member`
  objects and coordinates between them.
- **Persistence**: reading/writing structured data to JSON.

## Project structure

```
library_system/
├── models.py    # LibraryItem, Book, Magazine, Member classes
├── library.py   # Library class - manages collection + persistence
├── main.py      # CLI menu (entry point)
└── README.md
```

## Ideas to extend it (good for interview talking points)

- Add a `DVD` class to show a third subclass of `LibraryItem`
- Add fines for overdue items
- Swap JSON storage for SQLite
- Add unit tests with `pytest`
