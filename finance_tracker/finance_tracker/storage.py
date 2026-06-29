"""
storage.py
SQLite persistence layer for the finance tracker (uses Python's built-in
sqlite3 module - no extra install needed).
"""

import sqlite3
from models import Transaction


class Storage:
    def __init__(self, db_file="finance.db"):
        self.conn = sqlite3.connect(db_file)
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                note TEXT,
                date TEXT NOT NULL,
                txn_type TEXT NOT NULL
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                monthly_limit REAL NOT NULL
            )
        """)
        self.conn.commit()

    def save_transaction(self, t: Transaction):
        self.conn.execute(
            "INSERT INTO transactions (amount, category, note, date, txn_type) "
            "VALUES (?, ?, ?, ?, ?)",
            (t.amount, t.category, t.note, t.date, t.txn_type),
        )
        self.conn.commit()

    def save_budget(self, category, monthly_limit):
        self.conn.execute(
            "INSERT OR REPLACE INTO budgets (category, monthly_limit) VALUES (?, ?)",
            (category, monthly_limit),
        )
        self.conn.commit()

    def load_transactions(self):
        cursor = self.conn.execute(
            "SELECT amount, category, note, date, txn_type FROM transactions"
        )
        return [
            Transaction(amount=row[0], category=row[1], note=row[2],
                        txn_date=row[3], txn_type=row[4])
            for row in cursor.fetchall()
        ]

    def load_budgets(self):
        cursor = self.conn.execute("SELECT category, monthly_limit FROM budgets")
        return {row[0]: row[1] for row in cursor.fetchall()}

    def close(self):
        self.conn.close()
