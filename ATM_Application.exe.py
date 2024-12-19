import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import tkinter.simpledialog
import uuid
from tkinter import ttk


class BankATM:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to ATM")
        self.root.geometry("400x300")

        # Predefined accounts with necessary fields
        self.accounts = {
            "123456": {
                "pin": "1111",
                "name": "Subitha",
                "balance": 100000.0,
                "opening_balance": 100000.0,
                "transactions": [],
                "account_number": "123456",
                "mobile_number": "6385491293",
                "ifsc_code": "IFSC001",
                "branch_name": "IOB Vallioor",
                "branch_code": "VLR001",
                "atm_card": "1111222233334444",
                "daily_deposit": 0.0,
                "daily_reset": datetime.now(),
                "lockout_until": None,
                "failed_attempts": 0,
                "loan_accounts": {
                    "LN001": {
                        "loan_type": "Home Loan",
                        "loan_balance": 500000.0,
                        "loan_due_date": "2024-12-31",
                        "loan_minimum_due": 10000.0,
                        "loan_account": "LN001"

                    },
                    "LN002": {
                        "loan_type": "Personal Loan",
                        "loan_balance": 200000.0,
                        "loan_due_date": "2024-12-25",
                        "loan_minimum_due": 5000.0,
                        "loan_account": "LN002"
                    }
                },
                "bill_accounts": {
                    "Electricity": {
                        "provider": "State Electricity Board",
                        "due_date": "2024-12-31",
                        "reference_required": True,
                        "sample_account_id": "ELEC12345"
                    },
                    "Water":
                        {
                        "provider": "Municipal Water Supply",
                        "due_date": "2024-12-25",
                        "reference_required": True,
                        "sample_account_id": "WATER67890"
                    },
                    "Internet": {
                        "provider": "ISP Ltd.",
                        "due_date": "2024-12-20",
                        "reference_required": True,
                        "sample_account_id": "NET12345"
                    }
                }
            },
            "123457": {
                "pin": "2222",
                "name": "Ananth",
                "balance": 50000.0,
                "opening_balance": 50000.0,
                "transactions": [],
                "account_number": "123457",
                "mobile_number": "9043363293",
                "ifsc_code": "IFSC002",
                "branch_name": "TMB VLR",
                "branch_code": "VLR002",
                "atm_card": "5555666677778888",
                "daily_deposit": 0.0,
                "daily_reset": datetime.now(),
                "lockout_until": None,
                "failed_attempts": 0,
                "loan_accounts": {
                    "LN003": {
                        "loan_type": "Car Loan",
                        "loan_balance": 300000.0,
                        "loan_due_date": "2025-01-15",
                        "loan_minimum_due": 15000.0,
                        "loan_account": "LN003"

                    }
                },
                "bill_accounts": {
                    "Electricity": {
                        "provider": "State Electricity Board",
                        "due_date": "2024-12-31",
                        "reference_required": True,
                        "sample_account_id": "ELEC54321"
                    },
                    "Water": {
                        "provider": "Municipal Water Supply",
                        "due_date": "2024-12-25",
                        "reference_required": True,
                        "sample_account_id": "WATER09876"
                    },
                    "Internet": {
                        "provider": "ISP Ltd.",
                        "due_date": "2024-12-20",
                        "reference_required": True,
                        "sample_account_id": "NET45678"
                    }
                }
            }
        }

        # Main window widgets
        self.heading = tk.Label(self.root, text="Welcome to ATM", font=("Arial", 16, "bold"))
        self.heading.pack(pady=10)

        self.login_button = tk.Button(self.root, text="Login", font=("Arial", 12), command=self.show_login)
        self.login_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", font=("Arial", 12), command=self.root.quit)
        self.exit_button.pack(pady=10)

    def show_login(self):
        """ Show login window and hide main window. """
        self.root.withdraw()  # Hide main window permanently
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")
        self.login_window.geometry("400x300")
        self.login_window.protocol("WM_DELETE_WINDOW", self.root.quit)  # Close app on X button

        tk.Label(self.login_window, text="Enter Account Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.account_name_entry = tk.Entry(self.login_window, font=("Arial", 12))
        self.account_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.login_window, text="Enter PIN:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.pin_entry = tk.Entry(self.login_window, font=("Arial", 12), show="*")
        self.pin_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.login_window, text="Login", font=("Arial", 12), command=self.validate_login).grid(row=2, column=0, columnspan=2, pady=20)

    def validate_login(self):
        """ Validate login credentials and show main menu. """
        account_name = self.account_name_entry.get()
        pin = self.pin_entry.get()

        # Find account by name
        account = next((acc for acc in self.accounts.values() if acc["name"] == account_name), None)

        if not account:
            messagebox.showerror("Error", "Account not found.")
            return

        if account["lockout_until"] and datetime.now() < account["lockout_until"]:
            lockout_time = account["lockout_until"].strftime("%H:%M:%S")
            messagebox.showerror("Error", f"Account locked. Try again after {lockout_time}.")
            return

        if account["pin"] == pin:
            account["failed_attempts"] = 0  # Reset failed attempts
            self.login_window.destroy()  # Close login window
            self.show_main_menu(account)
        else:
            account["failed_attempts"] += 1
            if account["failed_attempts"] >= 3:
                account["lockout_until"] = datetime.now() + timedelta(hours=12)
                messagebox.showerror("Error", "Too many failed attempts. Account locked for 12 hours.")
            else:
                remaining_attempts = 3 - account["failed_attempts"]
                messagebox.showerror("Error", f"Invalid PIN. {remaining_attempts} attempt(s) remaining.")

    def show_main_menu(self, account):
        """ Show the main menu. """
        self.main_menu = tk.Toplevel(self.root)
        self.main_menu.title("Main Menu")
        self.main_menu.geometry("800x400")
        self.main_menu.protocol("WM_DELETE_WINDOW", self.root.quit)

        tk.Label(self.main_menu, text=f"Welcome, {account['name']}!", font=("Arial", 14, "bold")).pack(pady=10)

        button_frame = tk.Frame(self.main_menu)
        button_frame.pack(pady=20)

        # Buttons list
        actions = [
            "Cash Transfer", "Cash Withdrawal", "Balance Inquiries", "Mini Statement",
            "Deposit Cheques", "Recharge Your Mobile", "Pay Loan", "Deposit Cash",
            "Pay Bill", "Logout", "Exit"
        ]

        for i, action in enumerate(actions):
            btn = tk.Button(button_frame, text=action, font=("Arial", 12), width=20,
                            command=lambda a=action: self.perform_action(a, account))
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)

    def perform_action(self, action, account):
        """Perform the corresponding action."""
        self.reset_opening_balance(account)  # Ensure opening balance is up-to-date
        if action == "Logout":
            self.main_menu.destroy()
            self.show_login()
        elif action == "Exit":
            self.root.quit()
        elif action == "Balance Inquiries":
            self.show_balance(account)
        elif action == "Mini Statement":
            self.mini_statement(account)
        elif action == "Deposit Cash":
            self.deposit_cash(account)
        elif action == "Cash Withdrawal":
            self.cash_withdrawal(account)
        elif action == "Cash Transfer":
            self.open_cash_transfer_window(account)
        elif action == "Deposit Cheques":
            self.deposit_cheque(account)
        elif action == "Recharge Your Mobile":
            self.recharge_mobile(account)
        elif action == "Pay Loan":
            self.pay_loan(account)
        elif action =="Pay Bill":
            self.pay_bill(account)
        else:
            self.create_action_window(action, f"{action} functionality will be implemented soon!")

    def create_action_window(self, title, message, geometry="300x200"):
        """Create a simple pop-up window with a given title and message."""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("500x400")  # Set the window size

        # Add a label for the message
        label = tk.Label(window, text=message, font=("Arial", 12), justify="left", wraplength=350)
        label.pack(pady=10)

        # Add a button to close the window
        close_button = tk.Button(window, text="Close", command=window.destroy, font=("Arial", 12))
        close_button.pack(pady=10)

    def close_action_window(self, window):
        """ Close the action window and return to the main menu. """
        window.destroy()
        self.main_menu.deiconify()  # Show the main menu again

    # Placeholder methods for other features
    def show_balance(self, account):
        """ Display the current and opening balance. """
        self.reset_opening_balance(account)

        transactions = account.get("transactions", [])
        transaction_details = "\n".join([
            f"{t['type']} | Amount: INR {t['amount']:.2f} | Balance: INR {t['balance']:.2f} | Date: {t['time']}"
            for t in transactions
        ])

        messagebox.showinfo(
            "Account Balance",
            f"Account Name: {account['name']}\n"
            f"Account No: {account['account_number']}\n"
            f"Opening Balance: INR {account['opening_balance']:.2f}\n"
            f"Current Balance: INR {account['balance']:.2f}\n\n"
           # f"Transactions:\n{transaction_details}"
        )
    def open_cash_transfer_window(self, account):

        self.reset_opening_balance(account)

        # Create a new window for cash transfer
        window = tk.Toplevel(self.root)
        window.title("Cash Transfer")
        window.geometry("600x300")

        # Label for the title
        tk.Label(window, text="Cash Transfer", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Fields for input
        fields = ["PIN", "Account Name", "Beneficiary Account Number", "IFSC Code", "Transfer Amount"]
        entries = {}

        for i, field in enumerate(fields):
            label = tk.Label(window, text=field, font=("Arial", 12))
            label.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(window, font=("Arial", 12), width=30)
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            entries[field] = entry

        # Submit button to validate and process the transfer
        submit_btn = tk.Button(
            window, text="Submit", font=("Arial", 12),
            command=lambda: self.validate_cash_transfer(entries, window, account)
        )
        submit_btn.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

    def validate_cash_transfer(self, entries, window, account):
        self.reset_opening_balance(account)

        pin = entries["PIN"].get()
        account_name = entries["Account Name"].get()
        beneficiary_account_number = entries["Beneficiary Account Number"].get()
        ifsc_code = entries["IFSC Code"].get()
        transfer_amount = entries["Transfer Amount"].get()

        # Validate input
        from_account = self.accounts.get(account["account_number"])
        if from_account and from_account["pin"] == pin and from_account["name"] == account_name:
            # Initialize default keys if not present
            if "daily_total" not in from_account:
                from_account["daily_total"] = 0.0
            if "daily_reset" not in from_account:
                from_account["daily_reset"] = datetime.now()
            if "transactions" not in from_account:
                from_account["transactions"] = []
        else:
            messagebox.showerror("Error", "Invalid PIN or Account Name")
            return

        if beneficiary_account_number not in self.accounts:
            messagebox.showerror("Error", "Invalid Beneficiary Account Number")
            return

        to_account = self.accounts[beneficiary_account_number]
        if to_account["ifsc_code"] != ifsc_code:
            messagebox.showerror("Error", "Invalid IFSC Code")
            return

        try:
            transfer_amount = float(transfer_amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid Transfer Amount")
            return

        # Reset daily total if a new day
        if datetime.now() > from_account["daily_reset"] + timedelta(days=1):
            from_account["daily_total"] = 0.0
            from_account["daily_reset"] = datetime.now()

        if from_account["daily_total"] + transfer_amount > 50000:
            messagebox.showerror("Error", "Transfer amount exceeds daily limit of INR 50,000")
            return

        # Calculate monthly total
        monthly_total = sum(
            txn["amount"] for txn in from_account["transactions"]
            if datetime.now() - datetime.strptime(txn["time"], "%Y-%m-%d %H:%M:%S") <= timedelta(days=30)
        )

        if monthly_total + transfer_amount > 500000:
            messagebox.showerror("Error", "Transfer amount exceeds monthly limit of INR 5,00,000")
            return

        # Perform transfer
        if transfer_amount > from_account["balance"]:
            messagebox.showerror("Error", "Insufficient funds")
            return

        self.perform_cash_transfer(from_account, to_account, transfer_amount)

        # Display transfer slip
        self.display_transfer_slip(window, from_account, to_account, transfer_amount)

    def validate_cash_transfer(self, entries, window, account):
        self.reset_opening_balance(account)

        pin = entries["PIN"].get()
        account_name = entries["Account Name"].get()
        beneficiary_account_number = entries["Beneficiary Account Number"].get()
        ifsc_code = entries["IFSC Code"].get()
        transfer_amount = entries["Transfer Amount"].get()

        # Validate input
        from_account = self.accounts.get(account["account_number"])
        if from_account and from_account["pin"] == pin and from_account["name"] == account_name:
            # Initialize default keys if not present
            if "daily_total" not in from_account:
                from_account["daily_total"] = 0.0
            if "daily_reset" not in from_account:
                from_account["daily_reset"] = datetime.now()
            if "transactions" not in from_account:
                from_account["transactions"] = []
        else:
            messagebox.showerror("Error", "Invalid PIN or Account Name")
            return

        if beneficiary_account_number not in self.accounts:
            messagebox.showerror("Error", "Invalid Beneficiary Account Number")
            return

        to_account = self.accounts[beneficiary_account_number]
        if to_account["ifsc_code"] != ifsc_code:
            messagebox.showerror("Error", "Invalid IFSC Code")
            return

        try:
            transfer_amount = float(transfer_amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid Transfer Amount")
            return

        # Reset daily total if a new day
        if datetime.now() > from_account["daily_reset"] + timedelta(days=1):
            from_account["daily_total"] = 0.0
            from_account["daily_reset"] = datetime.now()

        if from_account["daily_total"] + transfer_amount > 50000:
            messagebox.showerror("Error", "Transfer amount exceeds daily limit of INR 50,000")
            return

        # Calculate monthly total
        monthly_total = sum(
            txn["amount"] for txn in from_account["transactions"]
            if datetime.now() - datetime.strptime(txn["time"], "%Y-%m-%d %H:%M:%S") <= timedelta(days=30)
        )

        if monthly_total + transfer_amount > 500000:
            messagebox.showerror("Error", "Transfer amount exceeds monthly limit of INR 5,00,000")
            return

        # Perform transfer
        if transfer_amount > from_account["balance"]:
            messagebox.showerror("Error", "Insufficient funds")
            return

        self.perform_cash_transfer(from_account, to_account, transfer_amount)

        # Display transfer slip
        self.display_transfer_slip(window, from_account, to_account, transfer_amount)

    def perform_cash_transfer(self, from_account, to_account, amount):
        """ Perform a cash transfer from one account to another. """
        self.reset_opening_balance(from_account)
        self.reset_opening_balance(to_account)

        transaction_id = str(uuid.uuid4())
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            if from_account["balance"] < amount:
                raise ValueError("Insufficient balance for the transfer.")

            # Update balances
            from_account["balance"] -= amount
            from_account["daily_total"] += amount
            to_account["balance"] += amount

            # Log transactions
            from_account["transactions"].append({
                "type": "Cash Transfer (Debit)",
                "transaction_id": transaction_id,
                "amount": -amount,
                "balance": from_account["balance"],
                "time": transaction_time,
                "to_account": to_account["account_number"]
            })

            to_account["transactions"].append({
                "type": "Cash Transfer (Credit)",
                "transaction_id": transaction_id,
                "amount": amount,
                "balance": to_account["balance"],
                "time": transaction_time,
                "from_account": from_account["account_number"]
            })

            messagebox.showinfo(
                "Success",
                f"Transfer successful!\n\nFrom Account: {from_account['account_number']}\n"
                f"To Account: {to_account['account_number']}\nAmount: INR {amount:.2f}\n"
                f"New Balance: INR {from_account['balance']:.2f}"
            )
        except ValueError as e:
            messagebox.showerror("Transfer Failed", str(e))

    def display_transfer_slip(self, window, from_account, to_account, amount):

        window.destroy()  # Close the transfer input window
        slip_window = tk.Toplevel(self.root)
        slip_window.title("Cash Transfer Slip")
        slip_window.geometry("700x300")

        # Title label
        tk.Label(slip_window, text="Cash Transfer Slip", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                          pady=10)

        # Details list for transaction
        details = [
            ("Beneficiary Name:", to_account['name']),
            ("Beneficiary Account Number:", to_account['account_number']),
            ("IFSC Code:", to_account['ifsc_code']),
            ("Transferred Amount:", f"INR {amount:.2f}"),
            ("Transfer From Account:", from_account['name']),
            ("Transaction ID:", to_account['transactions'][-1]['transaction_id']),
            ("Transaction Time:", to_account['transactions'][-1]['time'])
        ]

        # Display transaction details
        for i, (label, value) in enumerate(details, start=1):
            tk.Label(slip_window, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            tk.Label(slip_window, text=value, font=("Arial", 12)).grid(row=i, column=1, padx=10, pady=5, sticky="w")

    def cash_withdrawal(self, account):
        """ Perform a cash withdrawal for the given account. """
        self.reset_opening_balance(account)

        amount = self.get_amount("Withdraw Amount")  # Call the method to get amount

        if amount is None:  # User canceled the input
            return

        # Check if the withdrawal amount is greater than the account balance
        if amount > account['balance']:
            self.create_action_window("Withdrawal Failed", "Insufficient funds for this withdrawal.")
            return

        # Record the opening balance
        opening_balance = account['balance']

        # Deduct the amount from the account balance
        account['balance'] -= amount
        current_balance = account['balance']

        # Generate a transaction ID
        transaction_id = f"TXN{len(account['transactions']) + 1:04}"  # Auto-generate transaction ID

        # Record the transaction
        transaction = {
            "type": "Withdraw",
            "transaction_id": transaction_id,
            "amount": amount,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": current_balance
        }
        account['transactions'].append(transaction)

        # Display the withdrawal receipt
        self.create_action_window(
            "Withdrawal Successful",
            f"Withdrawal Slip\n\n\n"
            f"Account Name: {account['name']}\n\n"
            f"Account No: {account['account_number']}\n\n"
            f"Opening Balance: INR {opening_balance:.2f}\n\n"
            f"Withdrawn Amount: INR {amount:.2f}\n\n"
            f"Current Balance: INR {current_balance:.2f}"
        )

    def reset_opening_balance(self, account):
        """Reset the opening balance at the start of each day."""
        now = datetime.now()
        if now.date() > account["daily_reset"].date():  # Check if a new day has started
            account["daily_reset"] = now  # Update the daily reset timestamp
            account["opening_balance"] = account["balance"]  # Update the opening balance
            account["daily_total"] = 0.0  # Reset the daily total

    def reset_daily_total(self, account):
        """Reset daily_total if a new day has started."""
        if datetime.now().date() > account["daily_reset"].date():
            account["daily_total"] = 0.0
            account["daily_reset"] = datetime.now()

    def mini_statement(self, account):
        """Display the last 10 transactions and balances in a popup window."""
        self.reset_opening_balance(account)

        # Check if there are any transactions
        transactions = account.get("transactions", [])
        if not transactions:
            self.create_action_window("Mini Statement", "No recent transactions found.")
            return

        # Prepare transaction details
        transaction_details = "\n\n".join([
            (
                f"{t['type']} | ID: {t.get('transaction_id', 'N/A')} | "
                f"Amount: INR {abs(t['amount']):.2f} | "
                f"{'Bill Type: ' + t.get('bill_type', 'N/A') + ' | ' if t.get('type') == 'Bill Payment' else ''}"
                f"{'Ref: ' + t.get('bill_reference', 'N/A') + ' | ' if t.get('type') == 'Bill Payment' else ''}"
                f"Date: {t['time']} | Balance: INR {t['balance']:.2f} | "
                f"{'To Account: ' + str(t['to_account']) if 'to_account' in t else ''} "
                f"{'From Account: ' + str(t['from_account']) if 'from_account' in t else ''} | "
                f"{'Loan Type: ' + t.get('loan_type', 'N/A') if t.get('type') == 'Loan Payment' else ''}"
            )
            for t in transactions[-10:]  # Include only the last 10 transactions
        ])

        # Build the full message
        message = (
            f"Account Name: {account['name']}\n"
            f"Account No: {account['account_number']}\n"
            f"Opening Balance: INR {account['opening_balance']:.2f}\n\n"
            f"Transactions:\n{transaction_details}\n\n"
            f"Current Balance: INR {account['balance']:.2f}"
        )

        # Create a Toplevel window for the mini statement
        dialog = tk.Toplevel(self.root)
        dialog.title("Mini Statement")
        dialog.geometry("800x500")  # Adjust as needed

        label = tk.Label(dialog, text=message, font=("Arial", 10), justify="left", padx=10, pady=10)
        label.pack(padx=10, pady=10)

        close_button = tk.Button(dialog, text="Close", command=dialog.destroy, font=("Arial", 12))
        close_button.pack(pady=10)

        self.root.wait_window(dialog)  # Pause execution until dialog is closed


    def deposit_cash(self, account):
        """ Perform a deposit transaction for the given account. """
        self.reset_opening_balance(account)

        try:
            # Get the deposit amount
            amount = self.get_amount("Deposit Amount")
            if amount is None:
                return  # User canceled input

            # Validate that the deposit amount is positive
            if amount <= 0:
                self.create_action_window("Deposit Failed", "Invalid deposit amount. Please enter a positive value.")
                return

            # Record opening balance
            opening_balance = account['balance']

            # Update account balance
            account['balance'] += amount
            current_balance = account['balance']

            # Log the transaction
            transaction = {
                "type": "Deposit",
                "transaction_id": f"TXN{len(account['transactions']) + 1:04}",  # Auto-generate transaction ID
                "amount": amount,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "balance": current_balance
            }
            account['transactions'].append(transaction)

            # Display the deposit receipt
            self.create_action_window(
                "Deposit Slip",
                f"Deposit Slip \n\n\n"
                f"Account Name: {account['name']}\n\n"
                f"Account No: {account['account_number']}\n\n"
                f"Opening Balance: INR {opening_balance:.2f}\n\n"
                f"Deposited Amount: INR {amount:.2f}\n\n"
                f"Current Balance: INR {current_balance:.2f}"
            )
        except Exception as e:
            self.create_action_window("Error", f"An unexpected error occurred: {e}")

    def deposit_cheque(self, account):
        """ Deposit cheque functionality. """

        def submit_cheque():
            bank_name = bank_name_entry.get()
            amount = amount_entry.get()
            cheque_date = cheque_date_entry.get()
            beneficiary_account_no = beneficiary_account_no_entry.get()
            beneficiary_ifsc = beneficiary_ifsc_entry.get()

            try:
                # Validate inputs
                amount = float(amount)
                cheque_date = datetime.strptime(cheque_date, "%Y-%m-%d")
                if cheque_date > datetime.now():
                    raise ValueError("Cheque is postdated.")
                if amount <= 0:
                    raise ValueError("Amount must be greater than zero.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return

            # Validate if the beneficiary account exists
            beneficiary_account = self.accounts.get(beneficiary_account_no)
            if not beneficiary_account:
                messagebox.showerror("Error", "Invalid Beneficiary Account Number.")
                return

            # Generate unique transaction ID
            transaction_id = str(uuid.uuid4())

            # Update balances
            account["balance"] -= amount
            beneficiary_account["balance"] += amount

            # Log transaction for issuer account
            account["transactions"].append({
                "type": "Cheque Issued (Debit)",
                "transaction_id": transaction_id,
                "amount": -amount,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "balance": account["balance"],
                "to_account": beneficiary_account_no,
                "ifsc_code": beneficiary_ifsc
            })

            # Log transaction for beneficiary account
            beneficiary_account["transactions"].append({
                "type": "Cheque Deposit (Credit)",
                "transaction_id": transaction_id,
                "amount": amount,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "balance": beneficiary_account["balance"],
                "from_account": account["account_number"],
                "ifsc_code": beneficiary_ifsc
            })

            # Show success message
            messagebox.showinfo(
                "Success",
                f"Cheque deposit successful!\n\nFrom Account: {account['account_number']}\n"
                f"To Account: {beneficiary_account_no}\nAmount: INR {amount:.2f}\n"
                # f"New Balance: INR {beneficiary_account['balance']:.2f}"
            )
            cheque_window.destroy()

        cheque_window = tk.Toplevel(self.root)
        cheque_window.title("Deposit Cheque")
        cheque_window.geometry("400x400")

        # UI for cheque deposit
        tk.Label(cheque_window, text="Bank Name:", font=("Arial", 10)).pack(pady=5)
        bank_name_entry = tk.Entry(cheque_window, font=("Arial", 10))
        bank_name_entry.pack(pady=5)

        tk.Label(cheque_window, text="Amount:", font=("Arial", 10)).pack(pady=5)
        amount_entry = tk.Entry(cheque_window, font=("Arial", 10))
        amount_entry.pack(pady=5)

        tk.Label(cheque_window, text="Cheque Date (YYYY-MM-DD):", font=("Arial", 10)).pack(pady=5)
        cheque_date_entry = tk.Entry(cheque_window, font=("Arial", 10))
        cheque_date_entry.pack(pady=5)

        tk.Label(cheque_window, text="Beneficiary Account Number:", font=("Arial", 10)).pack(pady=5)
        beneficiary_account_no_entry = tk.Entry(cheque_window, font=("Arial", 10))
        beneficiary_account_no_entry.pack(pady=5)

        tk.Label(cheque_window, text="Beneficiary IFSC Code:", font=("Arial", 10)).pack(pady=5)
        beneficiary_ifsc_entry = tk.Entry(cheque_window, font=("Arial", 10))
        beneficiary_ifsc_entry.pack(pady=5)

        tk.Button(cheque_window, text="Submit", font=("Arial", 12), command=submit_cheque).pack(pady=20)

    def recharge_mobile(self, account):
        """Handle mobile recharge functionality with validation and mini statement update."""

        def submit_recharge():
            try:
                mobile_number = mobile_entry.get()
                amount = float(amount_entry.get())

                # Mobile number validation
                if not mobile_number.isdigit() or len(mobile_number) != 10:
                    raise ValueError("Invalid mobile number. It should be a 10-digit numeric value.")

                # Recharge amount validation
                if amount <= 0:
                    raise ValueError("Recharge amount must be greater than zero.")
                if amount > account["balance"]:
                    raise ValueError("Insufficient balance for the recharge.")

                # Deduct amount and record the transaction
                account["balance"] -= amount
                transaction_id = f"T{len(account['transactions']) + 1:04}"
                account["transactions"].append({
                    "transaction_id": transaction_id,
                    "type": "Mobile Recharge",
                    "amount": -amount,
                    "mobile_number": mobile_number,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "balance": account["balance"]
                })

                # Success message
                messagebox.showinfo(
                    "Success",
                    f"Mobile recharge of INR {amount:.2f} to {mobile_number} successful!"
                )

                # Optionally, print mini statement
               # self.print_mini_statement(account)

                # Close the recharge window
                recharge_window.destroy()

            except ValueError as e:
                messagebox.showerror("Error", str(e))

        # Create recharge window
        recharge_window = tk.Toplevel(self.root)
        recharge_window.title("Mobile Recharge")
        recharge_window.geometry("400x250")

        tk.Label(recharge_window, text="Enter Mobile Number:", font=("Arial", 12)).pack(pady=5)
        mobile_entry = tk.Entry(recharge_window, font=("Arial", 12))
        mobile_entry.pack(pady=5)

        tk.Label(recharge_window, text="Enter Recharge Amount:", font=("Arial", 12)).pack(pady=5)
        amount_entry = tk.Entry(recharge_window, font=("Arial", 12))
        amount_entry.pack(pady=5)

        tk.Button(recharge_window, text="Submit", font=("Arial", 12), command=submit_recharge).pack(pady=20)


    def get_amount(self, title):
        """
        Prompt the user to input a deposit amount. Returns a valid float or None if canceled.
        """

        def close_dialog(dialog, entry):
            """Handles dialog closing and validates the entered amount."""
            amount_str = entry.get()
            dialog.destroy()  # Close the dialog window
            if amount_str:  # Check if user entered a value
                try:
                    amount = float(amount_str)
                    if amount > 0:  # Ensure the amount is positive
                        self.valid_amount = amount
                    else:
                        self.create_action_window("Invalid Input", "Amount must be greater than zero.")
                        self.valid_amount = None
                except ValueError:
                    self.create_action_window("Invalid Input", "Please enter a valid numeric value.")
                    self.valid_amount = None
            else:
                self.valid_amount = None  # User canceled or entered no value

        # Initialize the valid amount variable
        self.valid_amount = None

        while self.valid_amount is None:  # Loop until a valid amount is provided
            # Create a custom Toplevel window for the dialog box
            dialog = tk.Toplevel(self.root)
            dialog.title(title)
            dialog.geometry("350x200")

            # Label to prompt the user for input
            label = tk.Label(dialog, text="Enter the amount:", font=("Arial", 12))
            label.pack(pady=10)

            # Entry widget for the amount input
            entry = tk.Entry(dialog, font=("Arial", 12))
            entry.pack(pady=10)

            # Button to submit the amount
            submit_button = tk.Button(
                dialog,
                text="Submit",
                command=lambda: close_dialog(dialog, entry),
                font=("Arial", 12)
            )
            submit_button.pack(pady=5)

            # Wait for the dialog to be closed
            self.root.wait_window(dialog)

        # Return the valid amount once obtained
        return self.valid_amount

    def pay_loan(self, account):
        """Handle loan repayment."""

        def update_loan_account_dropdown(event=None):
            """Update the loan account dropdown based on selected loan type."""
            selected_type = loan_type_combo.get()
            loan_accounts = [
                acc for acc, details in account.get("loan_accounts", {}).items()
                if details["loan_type"] == selected_type
            ]
            loan_account_combo["values"] = loan_accounts
            loan_account_combo.set("")  # Clear the previous selection

        def submit_payment():
            try:
                loan_account = loan_account_combo.get()
                payment_amount = float(payment_amount_entry.get())

                # Validate loan account
                if not loan_account:
                    raise ValueError("Please select a loan account.")
                if loan_account not in account.get("loan_accounts", {}):
                    raise ValueError("Invalid loan account number.")

                loan_details = account["loan_accounts"][loan_account]

                # Validate payment amount
                if payment_amount <= 0:
                    raise ValueError("Payment amount must be greater than zero.")
                if payment_amount > account["balance"]:
                    raise ValueError("Insufficient balance for loan repayment.")
                if payment_amount > loan_details["loan_balance"]:
                    raise ValueError("Payment amount exceeds loan balance.")

                # Deduct payment amount from account balance
                account["balance"] -= payment_amount
                loan_details["loan_balance"] -= payment_amount

                # Record the transaction
                transaction_id = f"T{len(account['transactions']) + 1:04}"
                loan_type = loan_details["loan_type"]  # Get loan type for the transaction
                account["transactions"].append({
                    "transaction_id": transaction_id,
                    "type": "Loan Payment",
                    "amount": -payment_amount,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "balance": account["balance"],
                    "to_account": loan_account,
                    "loan_type": loan_type  # Store the loan type in the transaction
                })

                # Success message
                messagebox.showinfo(
                    "Success",
                    f"Loan repayment of INR {payment_amount:.2f} to Loan Account {loan_account} was successful!\n"
                    f"Remaining Loan Balance: INR {loan_details['loan_balance']:.2f}"
                )
                pay_loan_window.destroy()

            except ValueError as e:
                messagebox.showerror("Error", str(e))

        # Create pay loan window
        pay_loan_window = tk.Toplevel(self.root)
        pay_loan_window.title("Pay Loan")
        pay_loan_window.geometry("400x400")

        # Loan type selection
        tk.Label(pay_loan_window, text="Select Loan Type:", font=("Arial", 12)).pack(pady=5)
        loan_type_var = tk.StringVar()
        loan_types = list({details["loan_type"] for details in account.get("loan_accounts", {}).values()})
        loan_type_combo = ttk.Combobox(pay_loan_window, textvariable=loan_type_var, font=("Arial", 12))
        loan_type_combo["values"] = loan_types
        loan_type_combo.bind("<<ComboboxSelected>>", update_loan_account_dropdown)
        loan_type_combo.pack(pady=5)

        # Loan account selection
        tk.Label(pay_loan_window, text="Select Loan Account:", font=("Arial", 12)).pack(pady=5)
        loan_account_var = tk.StringVar()
        loan_account_combo = ttk.Combobox(pay_loan_window, textvariable=loan_account_var, font=("Arial", 12))
        loan_account_combo.pack(pady=5)

        # Payment amount input
        tk.Label(pay_loan_window, text="Enter Payment Amount:", font=("Arial", 12)).pack(pady=5)
        payment_amount_entry = tk.Entry(pay_loan_window, font=("Arial", 12))
        payment_amount_entry.pack(pady=5)

        # Submit button
        tk.Button(pay_loan_window, text="Submit Payment", font=("Arial", 12), command=submit_payment).pack(pady=20)

    def get_loan_type(self, account, loan_account_id):
        """ Returns the loan type for a given loan account ID. """
        loan_accounts = account.get("loan_accounts", {})

        # Retrieve the loan account based on the provided loan account ID
        loan_account = loan_accounts.get(loan_account_id, {})  # Ensure we're getting the right account

        # Return the loan type, or 'N/A' if the loan account is not found
        return loan_account.get("loan_type", "N/A")

    def pay_bill(self, account):
        """Handle bill payment."""

        def update_reference_options(event):
            """Update the reference combo box options based on the selected bill type."""
            selected_bill_type = bill_type_var.get()
            if selected_bill_type in account.get("bill_accounts", {}):
                sample_id = account["bill_accounts"][selected_bill_type].get("sample_account_id", "")
                bill_reference_combo['values'] = [sample_id] if sample_id else ["No reference required"]
                bill_reference_combo.set("")  # Reset the combo box value

        def submit_payment():
            try:
                bill_type = bill_type_var.get()
                bill_reference = bill_reference_combo.get()
                payment_amount = float(payment_amount_entry.get())

                # Validate bill type
                if bill_type not in account.get("bill_accounts", {}):
                    raise ValueError("Invalid or unsupported bill type.")

                # Validate bill reference
                if account["bill_accounts"][bill_type].get("reference_required") and not bill_reference:
                    raise ValueError(f"Bill reference/account ID is required for {bill_type}.")
                if bill_reference and bill_reference != account["bill_accounts"][bill_type].get("sample_account_id"):
                    raise ValueError(
                        f"Invalid Bill Reference/Account ID. Example: {account['bill_accounts'][bill_type].get('sample_account_id')}")

                # Validate payment amount
                if payment_amount <= 0:
                    raise ValueError("Payment amount must be greater than zero.")
                if payment_amount > account["balance"]:
                    raise ValueError("Insufficient balance for bill payment.")

                # Deduct payment amount from account balance
                account["balance"] -= payment_amount

                # Record the transaction
                transaction_id = f"T{len(account['transactions']) + 1:04}"
                account["transactions"].append({
                    "transaction_id": transaction_id,
                    "type": "Bill Payment",
                    "amount": -payment_amount,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "balance": account["balance"],
                    "bill_type": bill_type,
                    "bill_reference": bill_reference
                })

                # Success message
                messagebox.showinfo(
                    "Success",
                    f"Bill payment of INR {payment_amount:.2f} for {bill_type} (Ref: {bill_reference}) was successful!\n"
                    f"Remaining Balance: INR {account['balance']:.2f}"
                )
                pay_bill_window.destroy()

            except ValueError as e:
                messagebox.showerror("Error", str(e))

        # Create pay bill window
        pay_bill_window = tk.Toplevel(self.root)
        pay_bill_window.title("Pay Bill")
        pay_bill_window.geometry("400x400")

        # Bill Type Selection
        tk.Label(pay_bill_window, text="Select Bill Type:", font=("Arial", 12)).pack(pady=5)
        bill_type_var = tk.StringVar()
        bill_type_combo = ttk.Combobox(pay_bill_window, textvariable=bill_type_var, font=("Arial", 12))
        bill_type_combo['values'] = list(account.get("bill_accounts", {}).keys())
        bill_type_combo.bind("<<ComboboxSelected>>", update_reference_options)
        bill_type_combo.pack(pady=5)

        # Bill Reference Selection
        tk.Label(pay_bill_window, text="Enter Bill Reference/Account ID:", font=("Arial", 12)).pack(pady=5)
        bill_reference_combo = ttk.Combobox(pay_bill_window, font=("Arial", 12))
        bill_reference_combo.pack(pady=5)

        # Payment Amount Input
        tk.Label(pay_bill_window, text="Enter Payment Amount:", font=("Arial", 12)).pack(pady=5)
        payment_amount_entry = tk.Entry(pay_bill_window, font=("Arial", 12))
        payment_amount_entry.pack(pady=5)

        # Submit Button
        tk.Button(pay_bill_window, text="Submit Payment", font=("Arial", 12), command=submit_payment).pack(pady=20)


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = BankATM(root)
    root.mainloop()
