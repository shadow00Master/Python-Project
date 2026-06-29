"""
models.py
Core OOP classes for the personal finance tracker.
"""

from datetime import date


class Transaction:
    """A single income or expense entry."""

    def __init__(self, amount, category, note="", txn_date=None, txn_type="expense"):
        if txn_type not in ("expense", "income"):
            raise ValueError("txn_type must be 'expense' or 'income'")
        self.amount = float(amount)
        self.category = category
        self.note = note
        self.date = txn_date or date.today().isoformat()
        self.txn_type = txn_type

    def __str__(self):
        sign = "-" if self.txn_type == "expense" else "+"
        return f"{self.date} | {sign}{self.amount:.2f} | {self.category} | {self.note}"


class Budget:
    """A monthly spending limit for one category."""

    def __init__(self, category, monthly_limit):
        self.category = category
        self.monthly_limit = float(monthly_limit)

    def is_exceeded(self, spent_amount):
        return spent_amount > self.monthly_limit


class Account:
    """Aggregates transactions and budgets, and reports balances."""

    def __init__(self, owner_name, starting_balance=0.0):
        self.owner_name = owner_name
        self.starting_balance = float(starting_balance)
        self.transactions = []
        self.budgets = {}  # category -> Budget

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def set_budget(self, category, monthly_limit):
        self.budgets[category] = Budget(category, monthly_limit)

    def balance(self):
        total = self.starting_balance
        for t in self.transactions:
            total += t.amount if t.txn_type == "income" else -t.amount
        return total

    def spent_by_category(self, category):
        return sum(
            t.amount for t in self.transactions
            if t.category == category and t.txn_type == "expense"
        )

    def budget_status(self):
        status = {}
        for category, budget in self.budgets.items():
            spent = self.spent_by_category(category)
            status[category] = {
                "limit": budget.monthly_limit,
                "spent": spent,
                "exceeded": budget.is_exceeded(spent),
            }
        return status
