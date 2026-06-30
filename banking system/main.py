import datetime

class Account:
    def __init__(self, name, acc_number, balance):
        self.owner_name = name
        self.acc_number = acc_number
        self.balance = balance
        self.transactions = []
    
    #custom function for amount validation
    def _Amount_check(self,amount):
        if amount <= 0:
            raise ValueError("Enter the correct amount(only positive number)")
        if not isinstance(amount, (int,float)):
            raise TypeError("Amount must be a number")

    def deposit(self, amount):            
        self._Amount_check(amount)
        self.balance += amount
        self.transactions.append(Transaction(len(self.transactions) +1, amount, "Deposit"))
        return True

    def withdraw_amount(self, amount):
        self._Amount_check(amount)
        if amount > self.balance:
            print("Insufficient balance")
            return False
        else:
            self.balance -= amount
            self.transactions.append(Transaction(len(self.transactions) +1, amount, "Withdraw"))
            return True
    
    def transfer(self, target_acc, amount):
        self._Amount_check(amount)
        if amount > self.balance:
            print("Insufficient balance")
            return None
        else:
            self.balance -= amount
            target_acc.balance += amount
            self.transactions.append(Transaction(len(self.transactions) +1, amount, f"Transfer to {target_acc.acc_number}"))
            target_acc.transactions.append(Transaction(len(target_acc.transactions) +1, amount, f"Transfer from {self.acc_number}"))
            return f"Transferred {amount} to {target_acc.owner_name}"
    
    #there show the address of atransections but not show the details 
    def print_statement(self):
        print(f"\n--- Statement for account {self.acc_number} ({self.owner_name}) ---")
        for t in self.transactions:
            print(t)
        print(f"--- Current Balance: {self.balance:.2f} ---")
      
    def get_blc(self):
        return f"Account balance: {self.balance}"
    
class SavingsAccount(Account):
    def __init__(self,name,acc_number,balance,interest_rate):
        super().__init__(name, acc_number, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest_amount = self.balance * (self.interest_rate / 100)
        self.deposit(interest_amount)
        # Manually adjust the last transaction type
        self.transactions[-1].type = "Interest Applied"
        return self.balance

class CurrentAccount(Account):
    def __init__(self, name, acc_number, balance,overdraft_limit):
        super().__init__(name, acc_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw_amount(self, amount):
        self._Amount_check(amount)
        if amount > (self.balance + self.overdraft_limit):
            print("Withdrawal amount exceeds overdraft limit.")
            return False
        else:
            self.balance -= amount
            self.transactions.append(Transaction(len(self.transactions) + 1, amount, "Withdraw"))
            return True

class Transaction:
    def __init__(self, transaction_id, transaction_amount, transaction_type, time_stamp=None):
        self.transaction_id = transaction_id
        self.amount = transaction_amount
        self.type = transaction_type
        if time_stamp is None:
            self.time_stamp = datetime.datetime.now()
        else:
            self.time_stamp = time_stamp
                
    def __str__(self):
        return f"ID: {self.transaction_id:03d} | Type: {self.type:<25} | Amount: {self.amount:8.2f} | Time: {self.time_stamp.strftime('%Y-%m-%d %H:%M:%S')}"

acc1 = SavingsAccount("Ahmad", "001", 5000, interest_rate=0.05)
acc2 = CurrentAccount("Ali", "002", 2000, overdraft_limit=1000)

accounts = {}
while True:

    print("\n-------Banking System-------")
    
    print("1: Deposit")
    print("2: Withdraw")
    print("3: Transfer")
    print("4: Print Statement")
    print("5: Create new Account")
    print("0: Exit")

    choice = input("Enter your choice: ")
    
    try:
        if choice == "1":
            acc_number = input("Enter your account number: ")
            if acc_number not in accounts:
                print("Account not found")
                continue
            amount = float(input("Enter the amount to deposit: "))
            if accounts[acc_number].deposit(amount):
                print(f"Successfully deposited {amount:.2f}. New balance is {accounts[acc_number].balance:.2f}")

        elif choice == "2":
            acc_number = input("Enter your account number: ")
            if acc_number not in accounts:
                print("Account not found")
                continue
            amount = float(input("Enter amount to withdraw: "))
            if accounts[acc_number].withdraw_amount(amount):
                print(f"Successfully withdrew {amount:.2f}. Remaining balance is {accounts[acc_number].balance:.2f}")

        elif choice == "3":
            acc_number = input("Enter your account number: ")
            if acc_number not in accounts:
                print("Account not found")
                continue
            
            to_acc_number = input("Enter account number to transfer to: ")
            if to_acc_number not in accounts:
                print("Recipient account not found")
                continue

            amount = float(input("Enter amount to transfer: "))
            
            target_account = accounts[to_acc_number]
            
            result = accounts[acc_number].transfer(target_account, amount)
            if result:
                print(result)

        elif choice == "4":
            acc_number = input("Enter your account number: ")
            if acc_number not in accounts:
                print("Account not found")
                continue
            accounts[acc_number].print_statement()

        elif choice == "5":
            acc_type = input("Enter account type (Saving/Current): ").lower()
            name = input("Enter your name: ")
            acc_number = input("Enter your account number: ")
            if acc_number in accounts:
                print("Account number already exists.")
                continue
            amount = float(input("Enter initial balance: "))
            
            if acc_type == "saving":
                interest_rate = float(input("Enter interest rate (%): "))
                accounts[acc_number] = SavingsAccount(name, acc_number, amount, interest_rate)
                print(f"Savings account created for {name} with number {acc_number}")

            elif acc_type == "current":
                overdraft_limit = float(input("Enter overdraft limit: "))
                accounts[acc_number] = CurrentAccount(name, acc_number, amount, overdraft_limit)
                print(f"Current account created for {name} with number {acc_number}")
            else:
                print("Invalid account type")

        elif choice == "0":
            print("Thanks for visiting")
            break

        else:
            print("Invalid input!, Try again")
    except ValueError as e:
        print(f"Error: {e}. Please enter a valid number.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
