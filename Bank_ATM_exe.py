import tkinter as tk
from tkinter import simpledialog
from datetime import datetime
import uuid


class BankAccount:
    def __init__(self, account_number, name, pin, initial_balance=0):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = initial_balance
        self.transactions = []  # Store transactions as a list of dictionaries

    def deposit(self, amount):
        opening_balance = self.balance
        self.balance += amount
        transaction_id = str(uuid.uuid4())
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({
            "type": "Deposit",
            "transaction_id": transaction_id,
            "amount": amount,
            "balance": self.balance,
            "time": transaction_time
        })
        return opening_balance, self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return False, self.balance  # Insufficient funds
        opening_balance = self.balance
        self.balance -= amount
        transaction_id = str(uuid.uuid4())
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({
            "type": "Withdraw",
            "transaction_id": transaction_id,
            "amount": amount,
            "balance": self.balance,
            "time": transaction_time
        })
        return True, opening_balance


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, name, pin, initial_balance=0):
        account_number = len(self.accounts) + 1
        account = BankAccount(account_number, name, pin, initial_balance)
        self.accounts[account_number] = account
        return account

    def authenticate(self, name, pin):
        for account in self.accounts.values():
            if account.name == name and account.pin == pin:
                return account
        return None


class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BANK ATM")
        self.root.geometry("400x300")  # Set the geometry of the main window
        self.bank = Bank()
        self.account = None
        self.create_initial_accounts()  # Create predefined accounts
        self.create_main_screen()

    def create_initial_accounts(self):
        # Predefined account creation with hardcoded values
        self.bank.create_account("Subitha", "1000", 5000.0)
        self.bank.create_account("Ananth", "1001", 10000.0)
        self.bank.create_account("Prithvi", "1002", 20000.0)

    def create_main_screen(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        # Add a heading label with red color
        heading_label = tk.Label(self.main_frame, text="Welcome to Our ATM", fg="red", font=("Arial", 16))
        heading_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(self.main_frame, text="Login", command=self.login, bg="lightgreen").grid(row=1, column=0, pady=10)
        tk.Button(self.main_frame, text="Exit", command=self.exit_app, bg="lightcoral").grid(row=1, column=1, pady=10)

    def exit_app(self):
        """This method will quit the application."""
        self.root.quit()

    def login(self):
        name = self.custom_askstring("Login", "Enter Account Name:")
        pin = self.custom_askstring("Login", "Enter PIN:", show="*")

        if not name or not pin or len(pin) != 4 or not pin.isdigit():
            self.show_custom_message("Error", "Invalid account name or PIN.")
            return

        self.account = self.bank.authenticate(name, pin)
        if self.account:
            self.show_operations()
        else:
            self.show_custom_message("Error", "Invalid account name or PIN.")

    def custom_askstring(self, title, prompt, show=""):
        """Custom input dialog with styling."""
        def submit():
            value = entry.get()
            if not value:
                self.show_custom_message("Error", "Input cannot be empty.")
            else:
                result.append(value)
                popup.destroy()

        result = []
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("500x300")
        popup.config(bg="lightgray")

        label = tk.Label(popup, text=prompt, bg="lightgray", font=("Arial", 12))
        label.grid(row=0, column=0, padx=10, pady=5)

        entry = tk.Entry(popup, show=show, font=("Arial", 12), width=20)
        entry.grid(row=1, column=0, padx=10, pady=5)

        button = tk.Button(popup, text="Submit", command=submit, bg="lightblue", font=("Arial", 12))
        button.grid(row=2, column=0, padx=10, pady=5)

        popup.wait_window(popup)
        return result[0] if result else None

    def show_operations(self):
        # Destroy the main screen
        self.main_frame.destroy()

        operations_frame = tk.Frame(self.root)
        operations_frame.pack(pady=10)

        def deposit():
            amount = self.get_amount("Deposit Amount")
            if amount is not None:
                opening_balance, current_balance = self.account.deposit(amount)
                self.show_custom_message("Deposit Slip", f"Account Name: {self.account.name}\n"
                                                         f"Account No: {self.account.account_number}\n"
                                                         f"Opening Balance: {opening_balance}\n"
                                                         f"Deposited Amount: {amount}\n"
                                                         f"Current Balance: {current_balance}")

        def withdraw():
            amount = self.get_amount("Withdraw Amount")
            if amount is not None:
                success, opening_balance = self.account.withdraw(amount)
                if success:
                    self.show_custom_message("Withdraw Slip", f"Account Name: {self.account.name}\n"
                                                              f"Account No: {self.account.account_number}\n"
                                                              f"Opening Balance: {opening_balance}\n"
                                                              f"Withdrawn Amount: {amount}\n"
                                                              f"Current Balance: {self.account.balance}")
                else:
                    self.show_custom_message("Error", "Insufficient balance.")

        def show_balance():
            self.show_custom_message("Account Balance", f"Account Name: {self.account.name}\n"
                                                        f"Account No: {self.account.account_number}\n"
                                                        f"Current Balance: {self.account.balance}")

        def mini_statement():
            transactions = self.account.transactions
            if not transactions:
                self.show_custom_message("Mini Statement", "No transactions found.")
                return
            details = "\n\n".join([f"{t['type']} | ID: {t['transaction_id']} | Amount: {t['amount']} | Date: {t['time']} | Balance: {t['balance']}"
                                  for t in transactions])
            opening_balance = transactions[0]['balance'] - transactions[0]['amount'] if transactions else self.account.balance
            self.show_custom_message("Mini Statement", f"Account Name: {self.account.name}\n"
                                                       f"Account No: {self.account.account_number}\n"
                                                       f"Opening Balance: {opening_balance}\n\n"
                                                       f"Transactions:\n{details}\n\n"
                                                       f"Current Balance: {self.account.balance}")

        def back_to_home():
            self.show_main_screen()  # Go back to the main screen

        tk.Button(operations_frame, text="Deposit", command=deposit, bg="lightgreen").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(operations_frame, text="Withdraw", command=withdraw, bg="lightblue").grid(row=0, column=1, padx=10, pady=10)
        tk.Button(operations_frame, text="Show Balance", command=show_balance, bg="lightyellow").grid(row=1, column=0, padx=10, pady=10)
        tk.Button(operations_frame, text="Mini Statement", command=mini_statement, bg="lightgray").grid(row=1, column=1, padx=10, pady=10)
        tk.Button(operations_frame, text="Back to Home", command=back_to_home, bg="lightcoral").grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def show_main_screen(self):
        """Function to show the main screen again."""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        tk.Button(self.main_frame, text="Login", command=self.login, bg="lightgreen").grid(row=0, column=0, pady=10)
        tk.Button(self.main_frame, text="Exit", command=self.exit_app, bg="lightcoral").grid(row=0, column=1, pady=10)

    def get_amount(self, prompt):
        try:
            amount = float(self.custom_askstring(prompt, f"Enter {prompt.lower()}:"))
            if amount <= 0:
                self.show_custom_message("Error", "Amount must be positive.")
                return None
            return amount
        except (ValueError, TypeError):
            self.show_custom_message("Error", "Invalid amount.")
            return None

    def show_custom_message(self, title, message):
        """Function to show a custom message box with a colored title bar."""
        popup = tk.Toplevel(self.root)
        popup.title(title)

        # Adjust the size based on the message length, and add padding to adjust the size
        padding = 100
        message_length = len(message)
        lines = message.split("\n")
        height = len(lines) * 30 + padding  # Estimate size based on number of lines
        width = max([len(line) for line in lines]) * 10 + padding
        popup.geometry(f"{width}x{height}")

        popup.config(bg="lightgray")

        # Simulated colored title bar
        title_label = tk.Label(popup, text=title, font=("Arial", 14), fg="white", bg="darkblue", padx=10, pady=5)
        title_label.pack(fill="x")

        # Label for message with left alignment
        message_label = tk.Label(popup, text=message, font=("Arial", 12), fg="black", bg="lightyellow", padx=10, pady=10, anchor="w")
        message_label.pack(pady=10, padx=10, fill="both", expand=True)

        # OK Button
        ok_button = tk.Button(popup, text="OK", command=popup.destroy, bg="lightblue")
        ok_button.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
