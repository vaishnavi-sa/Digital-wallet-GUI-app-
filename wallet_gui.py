import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
conn = sqlite3.connect("wallet.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    balance REAL
)
''')
conn.commit()

# Functions
def create_account():
    name = entry_name.get()
    if name:
        cursor.execute("INSERT INTO users (name, balance) VALUES (?, ?)", (name, 0))
        conn.commit()
        messagebox.showinfo("Success", "Account Created!")
    else:
        messagebox.showerror("Error", "Enter Name")

def add_money():
    name = entry_name.get()
    amount = entry_amount.get()

    if name and amount:
        cursor.execute("UPDATE users SET balance = balance + ? WHERE name = ?", (float(amount), name))
        conn.commit()
        messagebox.showinfo("Success", "Money Added!")
    else:
        messagebox.showerror("Error", "Enter all fields")

def send_money():
    sender = entry_name.get()
    receiver = entry_receiver.get()
    amount = entry_amount.get()

    cursor.execute("SELECT balance FROM users WHERE name = ?", (sender,))
    result = cursor.fetchone()

    if result and float(amount) <= result[0]:
        cursor.execute("UPDATE users SET balance = balance - ? WHERE name = ?", (float(amount), sender))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE name = ?", (float(amount), receiver))
        conn.commit()
        messagebox.showinfo("Success", "Transaction Successful!")
    else:
        messagebox.showerror("Error", "Insufficient Balance or Invalid User")

def check_balance():
    name = entry_name.get()
    cursor.execute("SELECT balance FROM users WHERE name = ?", (name,))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Balance", f"Balance: {result[0]}")
    else:
        messagebox.showerror("Error", "User not found")

# GUI
root = tk.Tk()
root.title("Digital Wallet App")
root.geometry("400x400")

tk.Label(root, text="Digital Wallet System", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Receiver Name").pack()
entry_receiver = tk.Entry(root)
entry_receiver.pack()

tk.Label(root, text="Amount").pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Button(root, text="Create Account", command=create_account).pack(pady=5)
tk.Button(root, text="Add Money", command=add_money).pack(pady=5)
tk.Button(root, text="Send Money", command=send_money).pack(pady=5)
tk.Button(root, text="Check Balance", command=check_balance).pack(pady=5)

tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()

conn.close()
