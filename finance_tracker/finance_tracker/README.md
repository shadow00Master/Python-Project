# Personal Finance Tracker + PSX Stock Watchlist

A command-line app to track income/expenses against monthly budgets, plus a
watchlist for PSX (Pakistan Stock Exchange) holdings with live price lookup.

## What it does

- Record income and expenses by category
- Set a monthly budget per category and see if you're over it
- Track PSX stocks you own (shares + average buy price)
- Pull a live price for each stock and calculate current value / profit-loss
- Persists everything in a local SQLite database (`finance.db`)

## How to run

```
pip install -r requirements.txt
python main.py
```

## A note on the live stock prices

`stocks.py` tries to fetch a live price from a public PSX data endpoint. If
that fails for any reason (no internet, PSX changes their endpoint, you're
behind a restrictive network), it asks you to type the price in manually so
the rest of the app keeps working. This is intentional — it's a realistic
example of building software that degrades gracefully instead of crashing
when an external dependency is unavailable.

## OOP concepts this demonstrates

- **Classes & composition**: `Account` holds a list of `Transaction` objects
  and a dict of `Budget` objects; `Watchlist` holds `PSXStock` objects.
- **Encapsulation**: balance and budget-status calculations live inside
  `Account`, not scattered through the CLI code.
- **Separation of concerns**: business logic (`models.py`), external data
  (`stocks.py`), and persistence (`storage.py`) are split into separate
  modules instead of one giant script.
- **Error handling**: input validation and graceful fallback when a network
  call fails.

## Project structure

```
finance_tracker/
├── models.py    # Transaction, Budget, Account classes
├── stocks.py    # PSXStock, Watchlist - live price fetch + manual fallback
├── storage.py   # SQLite persistence
├── main.py      # CLI menu (entry point)
└── requirements.txt
```

## Ideas to extend it (good for interview talking points)

- Add monthly spending charts with `matplotlib`
- Export transactions to CSV/Excel
- Add multiple accounts (e.g., cash vs. bank)
- Cache stock prices with a timestamp instead of fetching every time
