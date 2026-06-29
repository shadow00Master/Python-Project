

class Account:
    def __init__(self, name, acc_number, balance):
        self.Owner_name = name
        self.acc_number = acc_number
        self.balance = balance
    
    def _Amount_check(self,amount):
        if amount < 0:
            raise ValueError("Enter the correct amount(only positive number)")
        if not isinstance(amount, (int,float)):
            raise ValueError("Amount must be an integer")

    def deposit(self, amount):
            self._Amount_check(amount)
            self.balance += amount
            return f"Total balance:{self.balance}"

    def withdraw_amount(self, amount):
        self._Amount_check(amount)
        if amount > self.balance:
            print("Insufficient balance")
        else:
            self.balance -= amount
            return f"Balance:{self.balance}"
        
    def get_blc(self):
        return f"Account balance: {self.balance}"
    
class SavingsAccount(Account):
    def __init__(self,name,acc_number,balance,interest_rate):
        super().__init__(name, acc_number,balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        self.balance += self.balance *(self.interest_rate/100)
        return self.balance

class CurrentAccount(Account):
    def __init__(self, name, acc_number, balance,overdraft_limit):
        super().__init__(name, acc_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        self._Amount_check(amount)
        if (self.balance + self.overdraft_limit) < amount:
            return f"Insufficient balance"
        if (self.balance + self.overdraft_limit) > amount:
            self.balance += self.overdraft_limit
            self.balance -= amount
            return self.balance

class Transection:
    def __init__(self, transection_id, amount, type , time_stamp):
        self.transection_id = transection_id
        self.amount = amount
        self.type = type
        self.time_stamp = time_stamp

class Account:
    def __init__(self, name, acc_number, balance):
        self.owner_name = name
        self.acc_number = acc_number
        self.balance = balance
        self.transactions = []   # store Transaction objects

    def _amount_check(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number")

    def deposit(self, amount):
        self._amount_check(amount)
        self.balance += amount
        self.transactions.append(Transaction(len(self.transactions)+1, amount, "Deposit"))
        return f"Deposited {amount}. Balance: {self.balance}"

    def withdraw(self, amount):
        self._amount_check(amount)
        if amount > self.balance:
            return "Insufficient balance"
        self.balance -= amount
        self.transactions.append(Transaction(len(self.transactions)+1, amount, "Withdraw"))
        return f"Withdrew {amount}. Balance: {self.balance}"

    def transfer(self, target_account, amount):
        self._amount_check(amount)
        if amount > self.balance:
            return "Insufficient balance for transfer"
        self.balance -= amount
        target_account.balance += amount
        self.transactions.append(Transaction(len(self.transactions)+1, amount, f"Transfer to {target_account.acc_number}"))
        target_account.transactions.append(Transaction(len(target_account.transactions)+1, amount, f"Transfer from {self.acc_number}"))
        return f"Transferred {amount} to {target_account.owner_name}"
    
    def print_statement(self):
        for t in self.transactions:
            print(t)


acc1 = SavingsAccount("Ahmad", "001", 5000, interest_rate=0.05)
acc2 = CurrentAccount("Ali", "002", 2000, overdraft_limit=1000)
print(acc1.get_blc())
acc1.deposit(500)
print(acc1.get_blc())



