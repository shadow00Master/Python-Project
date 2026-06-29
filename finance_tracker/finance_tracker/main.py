"""
main.py
CLI for the Personal Finance Tracker with PSX Stock Watchlist.
Run: python main.py
"""

from models import Account, Transaction
from stocks import Watchlist
from storage import Storage


def print_menu():
    print("""
==== PERSONAL FINANCE TRACKER ====
1. Add Income
2. Add Expense
3. Set Budget for Category
4. Show Balance & Budget Status
5. Add Stock to Watchlist
6. Refresh & Show Watchlist
7. Save & Exit
""")


def main():
    storage = Storage()
    account = Account(owner_name="Bilal", starting_balance=0.0)
    account.transactions = storage.load_transactions()
    for category, limit in storage.load_budgets().items():
        account.set_budget(category, limit)

    watchlist = Watchlist()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                amount = float(input("Amount: "))
                category = input("Category (e.g., Salary, Freelance): ")
                note = input("Note (optional): ")
                t = Transaction(amount, category, note, txn_type="income")
                account.add_transaction(t)
                storage.save_transaction(t)
                print("Income recorded.")

            elif choice == "2":
                amount = float(input("Amount: "))
                category = input("Category (e.g., Food, Transport): ")
                note = input("Note (optional): ")
                t = Transaction(amount, category, note, txn_type="expense")
                account.add_transaction(t)
                storage.save_transaction(t)
                print("Expense recorded.")

            elif choice == "3":
                category = input("Category: ")
                limit = float(input("Monthly limit: "))
                account.set_budget(category, limit)
                storage.save_budget(category, limit)
                print("Budget set.")

            elif choice == "4":
                print(f"\nCurrent balance: {account.balance():.2f}")
                status = account.budget_status()
                if not status:
                    print("No budgets set yet.")
                for category, info in status.items():
                    flag = "OVER!" if info["exceeded"] else "OK"
                    print(f"  {category}: spent {info['spent']:.2f} / {info['limit']:.2f} [{flag}]")

            elif choice == "5":
                symbol = input("PSX symbol (e.g., LUCK, PPL): ")
                shares = int(input("Shares owned: "))
                avg_price = float(input("Average buy price: "))
                watchlist.add_stock(symbol, shares, avg_price)
                print("Stock added to watchlist.")

            elif choice == "6":
                if not watchlist.stocks:
                    print("Watchlist is empty. Add a stock first (option 5).")
                else:
                    watchlist.refresh_all()
                    for stock in watchlist.stocks.values():
                        print(stock)
                    print(f"Total portfolio value: {watchlist.total_value():.2f}")
                    print(f"Total profit/loss: {watchlist.total_profit_loss():.2f}")

            elif choice == "7":
                storage.close()
                print("Data saved. Goodbye!")
                break

            else:
                print("Invalid option, try again.")

        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
