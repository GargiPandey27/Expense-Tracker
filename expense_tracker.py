import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

expenses = []
monthly_budget = None
current_user = None


USERS_FILE = 'users.csv'
EXPENSES_FILE = 'expenses.csv'

def save_expenses_to_file():
    with open(EXPENSES_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'date', 'category', 'amount', 'description'])
        writer.writeheader()
        writer.writerows(expenses)

def load_expenses_from_file():
    if not os.path.exists(EXPENSES_FILE):
        return
    with open(EXPENSES_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['amount'] = float(row['amount'])
            expenses.append(row)

def save_user_to_file(username, password):
    with open(USERS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

def user_exists(username, password):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

def set_monthly_budget():
    global monthly_budget
    try:
        monthly_budget = float(budget_var.get())
        messagebox.showinfo("Success", f"Budget set to {monthly_budget}.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

def add_expense():
    global expenses
    date = date_var.get()
    category = category_var.get()
    description = description_var.get()
    try:
        amount = float(amount_var.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")
        return

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
        return

    expense = {
        'username': current_user,
        'date': date,
        'category': category,
        'amount': amount,
        'description': description
    }
    expenses.append(expense)
    save_expenses_to_file()
    messagebox.showinfo("Success", "Expense addaed successfully!")

def view_expenses():
    filtered_expenses = [e for e in expenses if e['username'] == current_user]
    display_expenses(filtered_expenses)

def filter_expenses_by_category():
    category = filter_category_var.get()
    filtered_expenses = [e for e in expenses if e['username'] == current_user and e['category'] == category]
    display_expenses(filtered_expenses)

def filter_expenses_by_date():
    date = filter_date_var.get()
    filtered_expenses = [e for e in expenses if e['username'] == current_user and e['date'] == date]
    display_expenses(filtered_expenses)

def display_expenses(filtered_expenses):
    expense_list.delete(*expense_list.get_children())
    for expense in filtered_expenses:
        expense_list.insert("", "end", values=(expense['date'], expense['category'], expense['amount'], expense['description']))

def track_budget():
    global monthly_budget
    if monthly_budget is None:
        messagebox.showerror("Error", "Please set your budget first.")
        return

    total_expenses = sum(e['amount'] for e in expenses if e['username'] == current_user)
    remaining_budget = monthly_budget - total_expenses

    if remaining_budget < 0:
        messagebox.showwarning("Budget Exceeded", f"You have exceeded your budget by {-remaining_budget:.2f}.")
    else:
        messagebox.showinfo("Budget", f"You have {remaining_budget:.2f} left for the month.")

def login():
    global current_user
    username = username_var.get()
    password = password_var.get()
    if user_exists(username, password):
        current_user = username
        messagebox.showinfo("Success", "Login successful!")
        show_main_menu()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def signup():
    username = username_var.get()
    password = password_var.get()
    if user_exists(username, password):
        messagebox.showerror("Error", "User already exists.")
    else:
        save_user_to_file(username, password)
        messagebox.showinfo("Success", "Signup successful! Please log in.")

def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Track-Ur-Expenses", font=("Arial", 24, "bold"), bg="grey", fg="white", anchor="center").pack(fill="x")

    login_frame = tk.Frame(root, bg="grey")
    login_frame.pack(pady=20)

    tk.Label(login_frame, text="Username:", bg="grey").grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(login_frame, textvariable=username_var).grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_frame, text="Password:", bg="grey").grid(row=1, column=0, padx=5, pady=5)
    tk.Entry(login_frame, textvariable=password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

    tk.Button(login_frame, text="Login", command=login,bg="skyblue").grid(row=2, column=0, padx=5, pady=10)
    tk.Button(login_frame, text="Signup", command=signup, bg="skyblue").grid(row=2, column=1, padx=5, pady=10)

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Track-Ur-Expenses", font=("Arial", 24, "bold"), bg="skyblue", fg="white", anchor="center").pack(fill="x")

    main_frame = tk.Frame(root, bg="grey")
    main_frame.pack(pady=20)

    tk.Label(main_frame, text="Date (YYYY-MM-DD):", bg="beige", anchor="center").grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(main_frame, textvariable=date_var, justify="center").grid(row=0, column=1, padx=5, pady=5)

    tk.Label(main_frame, text="Category:", bg="beige", anchor="center").grid(row=1, column=0, padx=5, pady=5)
    tk.Entry(main_frame, textvariable=category_var, justify="center").grid(row=1, column=1, padx=5, pady=5)

    tk.Label(main_frame, text="Amount:", bg="beige", anchor="center").grid(row=2, column=0, padx=5, pady=5)
    tk.Entry(main_frame, textvariable=amount_var, justify="center").grid(row=2, column=1, padx=5, pady=5)

    tk.Label(main_frame, text="Description:", bg="beige", anchor="center").grid(row=3, column=0, padx=5, pady=5)
    tk.Entry(main_frame, textvariable=description_var, justify="center").grid(row=3, column=1, padx=5, pady=5)

    tk.Button(main_frame, text="Add Expense", bg="beige", command=add_expense).grid(row=4, column=0, padx=5, pady=10)
    tk.Button(main_frame, text="View All Expenses", command=view_expenses).grid(row=4, column=1, padx=5, pady=10)


    tk.Label(main_frame, text="Set Monthly Budget:", bg="beige").grid(row=5, column=0, padx=5, pady=5)
    tk.Entry(main_frame, textvariable=budget_var).grid(row=5, column=1, padx=5, pady=5)
    tk.Button(main_frame, text="Set Budget", command=set_monthly_budget).grid(row=5, column=2, padx=5, pady=5)

    tk.Label(main_frame, text="Filter by Date:", bg="beige", anchor="center").grid(row=6, column=0, padx=5, pady=5)
    tk.Entry(main_frame, textvariable=filter_date_var, justify="center").grid(row=6, column=1, padx=5, pady=5)
    tk.Button(main_frame, text="Filter", command=filter_expenses_by_date).grid(row=6, column=2, padx=5, pady=10)


    tk.Label(main_frame, text="Filter by Category:", bg="beige", anchor="center").grid(row=7, column=0, padx=5, pady=5)
    tk.Entry(main_frame, textvariable=filter_category_var, justify="center").grid(row=7, column=1, padx=5, pady=5)
    tk.Button(main_frame, text="Filter", command=filter_expenses_by_category).grid(row=7, column=2, padx=5, pady=10)


    global expense_list
    expense_list = ttk.Treeview(main_frame, columns=("Date", "Category", "Amount", "Description"), show="headings")
    expense_list.heading("Date", text="Date")
    expense_list.heading("Category", text="Category")
    expense_list.heading("Amount", text="Amount")
    expense_list.heading("Description", text="Description")

    expense_list.column("Date", anchor="center", width=100)
    expense_list.column("Category", anchor="center", width=100)
    expense_list.column("Amount", anchor="center", width=100)
    expense_list.column("Description", anchor="center", width=200)

    expense_list.grid(row=8, column=0, columnspan=3, padx=5, pady=10)

    tk.Button(main_frame, text="View All Expenses", command=view_expenses).grid(row=9, column=0, padx=5, pady=10)
    tk.Button(main_frame, text="Track Budget", command=track_budget).grid(row=9, column=1, padx=5, pady=10)
    tk.Button(main_frame, text="Set Budget", command=set_monthly_budget).grid(row=9, column=2, padx=5, pady=10)


root = tk.Tk()
root.title("Personal Expense Tracker")

username_var = tk.StringVar()
password_var = tk.StringVar()
date_var = tk.StringVar()
category_var = tk.StringVar()
amount_var = tk.StringVar()
description_var = tk.StringVar()
filter_category_var = tk.StringVar()
filter_date_var = tk.StringVar()
budget_var = tk.StringVar()

load_expenses_from_file()
show_login_screen()
root.mainloop()
