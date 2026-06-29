"""
models.py
Core classes for the Library Management System.

Demonstrates: encapsulation, inheritance, polymorphism, dunder methods.
"""

from datetime import datetime, timedelta


class LibraryItem:
    """Base class for anything that can be borrowed from the library."""

    LOAN_DAYS = 14  # default loan period in days

    def __init__(self, item_id, title, author):
        self.item_id = item_id
        self.title = title
        self.author = author
        self._is_borrowed = False
        self._due_date = None

    @property
    def is_borrowed(self):
        return self._is_borrowed

    def borrow(self):
        if self._is_borrowed:
            raise ValueError(f"'{self.title}' is already borrowed.")
        self._is_borrowed = True
        self._due_date = datetime.now() + timedelta(days=self.LOAN_DAYS)
        return self._due_date

    def return_item(self):
        if not self._is_borrowed:
            raise ValueError(f"'{self.title}' was not borrowed.")
        self._is_borrowed = False
        self._due_date = None

    def is_overdue(self):
        if self._is_borrowed and self._due_date:
            return datetime.now() > self._due_date
        return False

    def __str__(self):
        status = "Borrowed" if self._is_borrowed else "Available"
        return f"[{self.item_id}] {self.title} by {self.author} - {status}"

    def __repr__(self):
        return f"LibraryItem({self.item_id!r}, {self.title!r})"


class Book(LibraryItem):
    """A standard book. Inherits borrow/return logic from LibraryItem."""

    def __init__(self, item_id, title, author, genre):
        super().__init__(item_id, title, author)
        self.genre = genre

    def __str__(self):
        return super().__str__() + f" | Genre: {self.genre}"


class Magazine(LibraryItem):
    """Magazines get a shorter loan period - polymorphism via override."""

    LOAN_DAYS = 7

    def __init__(self, item_id, title, author, issue_number):
        super().__init__(item_id, title, author)
        self.issue_number = issue_number

    def __str__(self):
        return super().__str__() + f" | Issue #{self.issue_number}"


class Member:
    """A library member who can borrow items, up to a limit."""

    MAX_BOOKS = 3

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_items = []

    def can_borrow(self):
        return len(self.borrowed_items) < self.MAX_BOOKS

    def __str__(self):
        return f"Member[{self.member_id}] {self.name} ({len(self.borrowed_items)} item(s) borrowed)"
