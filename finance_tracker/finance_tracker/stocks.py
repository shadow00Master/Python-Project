"""
stocks.py
Track a watchlist of PSX (Pakistan Stock Exchange) symbols.

NOTE on live prices: PSX's own website (https://dps.psx.com.pk) loads
intraday data through a public JSON endpoint. This module tries that
endpoint first. If it fails for any reason (no internet, symbol typo,
endpoint changed), it falls back to asking you to type the price in
manually so the rest of the app keeps working either way.
"""

import requests


class PSXStock:
    def __init__(self, symbol, shares_owned=0, avg_buy_price=0.0):
        self.symbol = symbol.upper()
        self.shares_owned = int(shares_owned)
        self.avg_buy_price = float(avg_buy_price)
        self.last_price = None

    def fetch_price(self):
        """Try to fetch a live price from PSX's public data endpoint."""
        url = f"https://dps.psx.com.pk/timeseries/int/{self.symbol}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            # The endpoint returns {"data": [[timestamp, price, volume], ...]}
            latest = data["data"][-1]
            self.last_price = float(latest[1])
        except Exception as e:
            print(f"Could not fetch live price for {self.symbol} ({e}).")
            manual = input(f"Enter current price for {self.symbol} manually: ").strip()
            self.last_price = float(manual) if manual else 0.0
        return self.last_price

    def current_value(self):
        if self.last_price is None:
            self.fetch_price()
        return self.last_price * self.shares_owned

    def profit_loss(self):
        if self.last_price is None:
            self.fetch_price()
        return (self.last_price - self.avg_buy_price) * self.shares_owned

    def __str__(self):
        price_str = f"{self.last_price:.2f}" if self.last_price is not None else "N/A"
        return (f"{self.symbol}: {self.shares_owned} shares @ avg "
                f"{self.avg_buy_price:.2f} | Last: {price_str}")


class Watchlist:
    def __init__(self):
        self.stocks = {}  # symbol -> PSXStock

    def add_stock(self, symbol, shares_owned=0, avg_buy_price=0.0):
        self.stocks[symbol.upper()] = PSXStock(symbol, shares_owned, avg_buy_price)

    def refresh_all(self):
        for stock in self.stocks.values():
            stock.fetch_price()

    def total_value(self):
        return sum(s.current_value() for s in self.stocks.values())

    def total_profit_loss(self):
        return sum(s.profit_loss() for s in self.stocks.values())
