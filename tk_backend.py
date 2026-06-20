"""Tkinter-safe wrappers around the existing console/backend logic.

These helpers avoid input()/print() and instead return (ok, message) / values.
"""

from __future__ import annotations


from database import mydb, db_query
from bank import Bank
from customer import Customer


import random


def signup_user(username: str, password: str, name: str, age: int, city: str):
    username = (username or "").strip()
    if not username:
        return False, "Username is required"

    if not password:
        return False, "Password is required"

    if not name:
        return False, "Name is required"

    if age < 0:
        return False, "Age must be non-negative"

    if not city:
        return False, "City is required"

    existing = db_query(
        f"SELECT username FROM customers where username = '{username}';"
    )
    if existing:
        return False, "Username already exists"

    # unique account number
    while True:
        account_number = int(random.randint(10000000, 99999999))
        temp = db_query(
            f"SELECT account_number FROM customers WHERE account_number = '{account_number}';"
        )
        if temp:
            continue
        break

    cobj = Customer(username, password, name, age, city, account_number)
    cobj.createuser()

    bobj = Bank(username, account_number)
    bobj.create_transaction_table()

    mydb.commit()
    return True, account_number


def signin_user(username: str, password: str):
    username = (username or "").strip()
    if not username:
        return False, "Username is required"
    if not password:
        return False, "Password is required"

    temp = db_query(f"SELECT username FROM customers where username = '{username}';")
    if not temp:
        return False, "Enter correct username"

    temp_pw = db_query(
        f"SELECT password FROM customers where username = '{username}';"
    )
    if not temp_pw:
        return False, "Account password missing"

    if temp_pw[0][0] != password:
        return False, "Wrong password"

    acct = db_query(
        f"SELECT account_number FROM customers WHERE username = '{username}';"
    )
    account_number = acct[0][0] if acct else None
    if account_number is None:
        return False, "Account number not found"

    return True, (username, account_number)


def get_balance(username: str) -> int:
    rows = db_query(f"SELECT balance FROM customers WHERE username = '{username}';")
    if not rows:
        raise ValueError("User not found")
    return int(rows[0][0])


def deposit_amount(username: str, account_number: int, amount: int) -> str:
    if amount <= 0:
        raise ValueError("Amount must be positive")

    bobj = Bank(username, account_number)

    bal_before = get_balance(username)
    bobj.deposit(amount)
    mydb.commit()
    bal_after = get_balance(username)

    return f"Deposited {amount}. Balance: {bal_before} -> {bal_after}"


def withdraw_amount(username: str, account_number: int, amount: int) -> str:
    if amount <= 0:
        raise ValueError("Amount must be positive")

    bal_before = get_balance(username)
    if amount > bal_before:
        return "Insufficient Balance Please Deposit Money"

    bobj = Bank(username, account_number)
    bobj.withdraw(amount)
    mydb.commit()
    bal_after = get_balance(username)

    return f"Withdrew {amount}. Balance: {bal_before} -> {bal_after}"


def transfer_funds(
    username: str, account_number: int, receiver: int, amount: int
) -> str:
    if amount <= 0:
        raise ValueError("Amount must be positive")

    if receiver == account_number:
        return "Receiver account must be different from sender account"

    bal_before = get_balance(username)
    if amount > bal_before:
        return "Insufficient Balance Please Deposit Money"

    # check receiver exists
    receiver_rows = db_query(
        f"SELECT balance FROM customers WHERE account_number = '{receiver}';"
    )
    if not receiver_rows:
        return "Account Number Does not Exists"

    bobj = Bank(username, account_number)
    bobj.fundtransfer(receiver, amount)
    mydb.commit()

    bal_after = get_balance(username)
    return f"Transferred {amount} to {receiver}. Balance: {bal_before} -> {bal_after}"

