def Amount_check(amount):
    if amount < 0 :
        raise("Enter valid amount")
    elif amount is not type(int):
        raise("Enter valid input")

def deposit(self, amount):
    Amount_check(amount)
    self.balance += self.amount
    return f"{self.balance} is your Total balance"