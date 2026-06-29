"""
library.py
The Library class manages the collection, members, and borrow/return logic.

Demonstrates: composition (Library "has" Items and Members), data validation,
and persistence using JSON.
"""

import json
import os
from models import Book, Magazine, Member


class Library:
    def __init__(self, data_file="library_data.json"):
        self.data_file = data_file
        self.items = {}      # item_id -> LibraryItem
        self.members = {}    # member_id -> Member
        self.load()

    # ---------- Item management ----------
    def add_book(self, item_id, title, author, genre):
        self.items[item_id] = Book(item_id, title, author, genre)

    def add_magazine(self, item_id, title, author, issue_number):
        self.items[item_id] = Magazine(item_id, title, author, issue_number)

    def remove_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
        else:
            raise KeyError(f"No item with id {item_id}")

    # ---------- Member management ----------
    def add_member(self, member_id, name):
        self.members[member_id] = Member(member_id, name)

    # ---------- Borrowing logic ----------
    def borrow_item(self, member_id, item_id):
        member = self._get_member(member_id)
        item = self._get_item(item_id)

        if not member.can_borrow():
            raise ValueError(f"{member.name} has reached the borrow limit ({Member.MAX_BOOKS}).")

        due_date = item.borrow()
        member.borrowed_items.append(item_id)
        return due_date

    def return_item(self, member_id, item_id):
        member = self._get_member(member_id)
        item = self._get_item(item_id)

        item.return_item()
        if item_id in member.borrowed_items:
            member.borrowed_items.remove(item_id)

    def list_available(self):
        return [item for item in self.items.values() if not item.is_borrowed]

    def list_overdue(self):
        return [item for item in self.items.values() if item.is_overdue()]

    # ---------- Persistence ----------
    def save(self):
        data = {
            "items": [
                {
                    "type": "Magazine" if isinstance(item, Magazine) else "Book",
                    "item_id": item.item_id,
                    "title": item.title,
                    "author": item.author,
                    "extra": item.issue_number if isinstance(item, Magazine) else item.genre,
                    "is_borrowed": item.is_borrowed,
                }
                for item in self.items.values()
            ],
            "members": [
                {
                    "member_id": m.member_id,
                    "name": m.name,
                    "borrowed_items": m.borrowed_items,
                }
                for m in self.members.values()
            ],
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not os.path.exists(self.data_file):
            return
        with open(self.data_file, "r") as f:
            data = json.load(f)

        for item_data in data.get("items", []):
            if item_data["type"] == "Magazine":
                item = Magazine(item_data["item_id"], item_data["title"],
                                 item_data["author"], item_data["extra"])
            else:
                item = Book(item_data["item_id"], item_data["title"],
                            item_data["author"], item_data["extra"])
            item._is_borrowed = item_data["is_borrowed"]
            self.items[item.item_id] = item

        for m_data in data.get("members", []):
            member = Member(m_data["member_id"], m_data["name"])
            member.borrowed_items = m_data["borrowed_items"]
            self.members[member.member_id] = member

    # ---------- Helpers ----------
    def _get_item(self, item_id):
        if item_id not in self.items:
            raise KeyError(f"No item with id {item_id}")
        return self.items[item_id]

    def _get_member(self, member_id):
        if member_id not in self.members:
            raise KeyError(f"No member with id {member_id}")
        return self.members[member_id]
