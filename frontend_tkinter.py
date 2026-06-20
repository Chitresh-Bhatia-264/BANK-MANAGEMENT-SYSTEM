
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from tk_backend import (
    signup_user,
    signin_user,
    get_balance,
    deposit_amount,
    withdraw_amount,
    transfer_funds,
)


class BankApp(tb.Window):

    def __init__(self):
        super().__init__(themename="flatly")

        self.title("🏦 CHITRESH BANKING SYSTEM")
        self.geometry("900x650")
        self.minsize(850, 600)

        self.current_user = None
        self.current_account_number = None

        self.center_window()

        self.build_login_ui()

    def center_window(self):
        self.update_idletasks()

        width = 900
        height = 650

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ==================================
    # LOGIN PAGE
    # ==================================

    def build_login_ui(self):

        self.clear()

        container = tb.Frame(self)
        container.pack(expand=True)

        card = tb.Labelframe(
            container,
            text=" Secure Login ",
            bootstyle="primary",
            padding=25
        )
        card.pack()

        tb.Label(
            card,
            text="🏦 CHITRESH BANK",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(10, 5))

        tb.Label(
            card,
            text="Secure Digital Banking Platform",
            font=("Segoe UI", 10)
        ).pack(pady=(0, 20))

        self.login_username = tb.Entry(card, width=35)
        self.login_username.pack(pady=8)
        self.login_username.insert(0, "Username")

        self.login_password = tb.Entry(card, width=35, show="*")
        self.login_password.pack(pady=8)
        self.login_password.insert(0, "")

        tb.Button(
            card,
            text="🔐 Sign In",
            bootstyle="success",
            width=25,
            command=self.on_signin
        ).pack(pady=15)

        tb.Button(
            card,
            text="Create New Account",
            bootstyle="info-outline",
            width=25,
            command=self.build_signup_ui
        ).pack()



    def build_signup_ui(self):

        self.clear()

        frame = tb.Frame(self)
        frame.pack(expand=True)

        card = tb.Labelframe(
            frame,
            text=" Create Account ",
            bootstyle="success",
            padding=25
        )
        card.pack()

        entries = {}

        fields = [
            "Username",
            "Password",
            "Full Name",
            "Age",
            "City"
        ]

        for field in fields:

            tb.Label(card, text=field).pack(anchor="w")

            show = "*" if field == "Password" else ""

            ent = tb.Entry(card, width=40, show=show)
            ent.pack(pady=(0, 10))

            entries[field] = ent

        self.signup_entries = entries

        tb.Button(
            card,
            text="Create Account",
            bootstyle="success",
            width=25,
            command=self.on_signup
        ).pack(pady=10)

        tb.Button(
            card,
            text="Back",
            bootstyle="secondary-outline",
            width=25,
            command=self.build_login_ui
        ).pack()


    def build_dashboard(self):

        self.clear()

        main = tb.Frame(self, padding=20)
        main.pack(fill=BOTH, expand=True)

        top = tb.Frame(main)
        top.pack(fill=X)

        tb.Label(
            top,
            text=f"Welcome, {self.current_user}",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tb.Label(
            top,
            text=f"Account Number: {self.current_account_number}"
        ).pack(anchor="w")

        balance = get_balance(self.current_user)

        balance_card = tb.Labelframe(
            main,
            text=" Account Balance ",
            bootstyle="primary",
            padding=20
        )
        balance_card.pack(fill=X, pady=20)

        self.balance_var = tk.StringVar(
            value=f"₹ {balance:,.2f}"
        )

        tb.Label(
            balance_card,
            textvariable=self.balance_var,
            font=("Segoe UI", 28, "bold")
        ).pack()

        services = tb.Labelframe(
            main,
            text=" Banking Services ",
            bootstyle="info",
            padding=15
        )
        services.pack(fill=X)

        tb.Button(
            services,
            text="📊 Check Balance",
            bootstyle="primary",
            command=self.on_balance
        ).pack(fill=X, pady=5)

        tb.Button(
            services,
            text="💰 Deposit Money",
            bootstyle="success",
            command=self.on_deposit_open
        ).pack(fill=X, pady=5)

        tb.Button(
            services,
            text="💸 Withdraw Money",
            bootstyle="warning",
            command=self.on_withdraw_open
        ).pack(fill=X, pady=5)

        tb.Button(
            services,
            text="🔄 Fund Transfer",
            bootstyle="info",
            command=self.on_transfer_open
        ).pack(fill=X, pady=5)

        tb.Button(
            main,
            text="Logout",
            bootstyle="danger",
            command=self.build_login_ui
        ).pack(pady=20)



    def on_signup(self):

        try:
            username = self.signup_entries["Username"].get().strip()
            password = self.signup_entries["Password"].get().strip()
            name = self.signup_entries["Full Name"].get().strip()
            age = int(self.signup_entries["Age"].get())
            city = self.signup_entries["City"].get().strip()

            ok, result = signup_user(
                username,
                password,
                name,
                age,
                city
            )

            if ok:
                messagebox.showinfo(
                    "Success",
                    f"Account Created\nAccount No: {result}"
                )
                self.build_login_ui()

            else:
                messagebox.showerror("Error", result)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Age must be numeric"
            )

    def on_signin(self):

        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        ok, result = signin_user(username, password)

        if ok:
            self.current_user, self.current_account_number = result
            self.build_dashboard()
        else:
            messagebox.showerror("Login Failed", result)


    def refresh_balance(self):
        balance = get_balance(self.current_user)
        self.balance_var.set(f"₹ {balance:,.2f}")

    def on_balance(self):
        self.refresh_balance()

 

    def on_deposit_open(self):

        amount = tb.dialogs.Querybox.get_integer(
            "Deposit",
            "Enter Amount"
        )

        if amount:

            msg = deposit_amount(
                self.current_user,
                self.current_account_number,
                amount
            )

            self.refresh_balance()

            messagebox.showinfo("Success", msg)



    def on_withdraw_open(self):

        amount = tb.dialogs.Querybox.get_integer(
            "Withdraw",
            "Enter Amount"
        )

        if amount:

            msg = withdraw_amount(
                self.current_user,
                self.current_account_number,
                amount
            )

            self.refresh_balance()

            messagebox.showinfo("Success", msg)


    def on_transfer_open(self):

        receiver = tb.dialogs.Querybox.get_integer(
            "Transfer",
            "Receiver Account Number"
        )

        amount = tb.dialogs.Querybox.get_integer(
            "Transfer",
            "Amount"
        )

        if receiver and amount:

            msg = transfer_funds(
                self.current_user,
                self.current_account_number,
                receiver,
                amount
            )

            self.refresh_balance()

            messagebox.showinfo("Success", msg)


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()
