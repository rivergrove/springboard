# structure for menu inspired by code written by Reinderien: https://codereview.stackexchange.com/questions/255951/simple-banking-system-with-python

import uuid
import logging
logging.basicConfig(filename='logs/log_file.txt', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

class BalanceError(Exception): pass
class WithdrawError(Exception): pass
class DepositError(Exception): pass
class InterestRateError(Exception): pass
class AccountError(Exception): pass
class AmountError(Exception): pass
class PeriodError(Exception): pass

class Menu:
    '''This is a class for a menu.'''
    def multiple_choice_screen(self):
        '''This is a function that creates a starting screen for the menu.'''
        prompt = '\n'.join(
            f'{i}) {name}'
            for i, (name, fun) in enumerate(self.menu)
        ) + '\n'

        while True:
            choice = input(prompt)

            try:
                name, fun = self.menu[int(choice)]
            except ValueError:
                print('Invalid integer entered')
            except IndexError:
                print('Choice out of range')
            else:
                if fun(self):
                    break

class BankAccount: 
    '''This is a class for a bank account.'''
    def __init__(self, account_number:int, balance:float=0):
        '''This is a constructor for the bank account class.'''
        if balance < 0:
            raise BalanceError("Balance has to be non-negative!")
        if account_number < 0:
            raise AccountError("Invalid account_number.")
        else:
            self.balance = balance
    def withdraw(self, amount):
        '''This function withdraws an amount from the account balance.'''
        if amount < 0:
            raise WithdrawError("Amount has to be non-negative!")
        else:
            self.amount = amount
            self.balance -= self.amount
    def deposit(self, amount):
        '''This function deposits an amount to the account balance.'''
        if amount < 0:
            raise DepositError("Amount has to be non-negative!")
        else:
            self.amount = amount
            self.balance += self.amount

# class SavingsAccount(BankAccount): 
#     '''This is a class for a savings account, a type of bank account.'''
#     def __init__(self, account_number:int, balance:float=0, interest_rate:float=0.01):
#         '''This is a constructor for the savings account class.'''
#         if balance < 0:
#             raise BalanceError("Balance has to be non-negative!")
#         if account_number < 0:
#             raise AccountError("Invalid account_number.")
#         if interest_rate < 0:
#             raise InterestRateError("Interest Rate must be non-negative!")
#         else:
#             self.interest_rate, self.balance = interest_rate, balance

#     def compute_interest(self, n_periods = 1):
#         '''This is a function that returns the interest added to the account balance after n periods.'''
#         return (self.balance * (1 + self.interest_rate) ** n_periods - 1) - self.balance

class CheckingAccount(BankAccount):
    '''This is a class for a checking account, a type of bank account.'''
    def __init__(self, account_number:int, balance:float=100, minimum_balance:float=100):
        '''This is a constructor for the checking account class.'''
        if balance < 0:
            raise BalanceError("Balance has to be non-negative!")
        if account_number < 0:
            raise AccountError("Invalid account_number.")
        if balance < minimum_balance:
            raise BalanceError("Balance must exceed minimum balance!")
        else:
            self.account_number, self.minimum_balance, self.balance = account_number, minimum_balance, balance

class BankingMenu(Menu):
    '''This is a class for a banking menu.'''
    def __init__(self):
        '''This is a constructor for the banking menu class.'''
        self.accounts: Dict[str, CheckingAccount] = {}

    def create_account(self):
        '''This is a function that creates a checking account.'''
        choice = input('Enter your starting balance:\n')
        
        try:
            self.starting_balance = int(choice)
            self.account_number = uuid.uuid4().int
            self.accounts[self.account_number] = CheckingAccount(account_number = self.account_number, balance = self.starting_balance)
            print('starting_balance: ' + str(self.starting_balance) + '\n' + 'account_number: ' + str(self.account_number))
        except ValueError:
            print('Please enter an integer.')
        
    def view_accounts(self):
        '''This is a function to view all accounts and balances.'''
        print([('account number: ' + str(self.accounts[account].account_number), 'balance: ' + str(self.accounts[account].balance)) for account in self.accounts])

    def deposit(self):
        '''This is a function that deposits into an account.'''
        self.amount = input('Enter amount to deposit:\n')
        self.account = input('Enter account number:\n')
        
        try:
            self.deposit = int(self.amount)
            self.accounts[int(self.account)].deposit(self.deposit)
            print('$' + str(self.deposit) + ' has been deposited.')
        except ValueError:
            print('Please enter an integer.')
        
    def withdraw(self):
        '''This is a function that withdraws from an account.'''
        self.amount = input('Enter amount to withdraw:\n')
        self.account = input('Enter account number:\n')
        
        try:
            self.withdraw = int(self.amount)
            self.accounts[int(self.account)].withdraw(self.withdraw)
            print('$' + str(self.withdraw) + ' has been withdrawn.')
        except ValueError:
            print('Please enter an integer.')
        
    def exit(self) -> bool:
        '''This is a function to exit the banking menu.'''
        print('Thank you for banking with Pybank!')
        return True

    menu = (
        ('Exit', exit),
        ('Create savings account', create_account),
        ('View accounts', view_accounts),
        ('Deposit', deposit),
        ('Withdraw', withdraw)
    )

BankingMenu().multiple_choice_screen()

# class Customer:
#     '''This is a class for a bank customer.'''
#     def __init__(self, name:str, address:str, phone:int, email:str, password:str):
#         '''This is a constructor for the customer class.'''
#         self.name, self.address, self.email, self.phone, self.password = name, address, email, phone, password

# class Employee:
#     '''This is a class for a bank employee.'''
#     def __init__(self, name:str, department:str, title:str):
#         '''This is a constructor for the employee class.'''
#         self.name, self.department, self.title = name, department, title

# class Loan:
#     '''This is a class for a loan given from a bank employee to a bank customer.'''
#     def __init__(self, amount:float, interest_rate:float=0.05):
#         '''This is a constructor for the loan class.'''
#         if amount <= 0:
#             raise AmountError("Amount has to be positive!")
#         if interest_rate < 0:
#             raise InterestRateError("Interest rate must be non-negative!")
#         else:
#             self.amount, self.interest_rate, self.remaining_amount = amount, interest_rate, amount

#     def compute_interest(self, n_periods:int = 1):
#         '''This is a function that returns the interest owed from the loan after n periods.'''
#         if n_periods < 1:
#             raise PeriodError("Must enter more than 0 periods.")
#         return (self.remaining_amount * (1 + self.interest_rate) ** n_periods - 1) - self.remaining_amount

#     def pay_loan(self, amount:float):
#         '''This is a function that subtracts the paid amount from the remaining amount due on the loan.'''
#         if amount <= 0:
#             raise AmountError("Amount has to be positive!")
#         if self.remaining_amount < amount:
#             self.remaining_amount = 0
#         else:
#             self.remaining_amount -= amount       

# class CreditCard:
#     '''This is a class for a credit card issued to a bank customer.'''
#     def __init__(self, monthly_minimum_payment:float, monthly_interest_rate:float = 0.1):
#         '''This is a constructor for the credit card class.'''
#         if monthly_minimum_payment < 0:
#             raise AmountError("Amount has to be positive!")
#         if monthly_interest_rate < 0:
#             raise InterestRateError("Interest rate must be non-negative!")
#         self.monthly_minimum_payment, self.monthly_interest_rate = monthly_minimum_payment, monthly_interest_rate
        
#     amt_owed = 0

#     def pay_credit_card(self, amount:float):
#         '''This is a function that deducts the paid amount from the amount owed on the credit card.'''
#         if amount <= 0:
#             raise AmountError("Amount must be positive!")
#         else:
#             self.amt_owed -= amount

#     def compute_interest(self, n_periods:int = 1):
#         '''This is a function that returns the credit card interest owed after n periods.'''
#         if n_periods < 1:
#             raise PeriodError("Must enter more than 0 periods.")
#         else:
#             return (self.amt_owed * (1 + self.interest_rate) ** n_periods - 1) - self.amt_owed