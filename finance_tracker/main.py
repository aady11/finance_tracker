import json
import os
from datetime import datetime

EXPENSE_FILE = "expenses.json"
BUDGET_FILE = "budget.json"

# ---------- DATA HANDLING ----------

def load_data():
    if os.path.exists(EXPENSE_FILE):
        try:
            with open(EXPENSE_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []

def save_data(data):
    with open(EXPENSE_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_budget():
    if os.path.exists(BUDGET_FILE):
        try:
            with open(BUDGET_FILE, "r") as file:
                return json.load(file).get("budget", 0)
        except:
            return 0
    return 0

def save_budget(amount):
    with open(BUDGET_FILE, "w") as file:
        json.dump({"budget": amount}, file)

# ---------- FEATURES ----------

def add_expense(data):
    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category: ").lower()

        expense = {
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        data.append(expense)
        save_data(data)
        print("✅ Expense added!")
    except:
        print("❌ Invalid input")

def view_total(data):
    current_month = datetime.now().strftime("%Y-%m")
    total = 0

    for item in data:
        if "date" in item and item["date"].startswith(current_month):
            total += float(item["amount"])

    budget = load_budget()

    print(f"\n💰 This Month Spending: {total}")

    if budget > 0:
        print(f"🎯 Budget: {budget}")
        if total > budget:
            print("⚠️ You crossed your budget!")
        else:
            print(f"✅ Remaining: {budget - total}")

def view_by_category(data):
    current_month = datetime.now().strftime("%Y-%m")
    summary = {}

    for item in data:
        if "date" in item and item["date"].startswith(current_month):
            cat = item.get("category", "unknown")
            summary[cat] = summary.get(cat, 0) + float(item["amount"])

    print("\n📊 This Month by Category:")
    for cat, amt in summary.items():
        print(f"{cat}: {amt}")

def view_all(data):
    if not data:
        print("No expenses found.")
        return

    print("\n📋 All Expenses:")
    for i, item in enumerate(data):
        print(f"{i+1}. {item.get('category')} - {item.get('amount')} ({item.get('date')})")

def delete_expense(data):
    view_all(data)
    try:
        index = int(input("Enter number to delete: ")) - 1
        if 0 <= index < len(data):
            data.pop(index)
            save_data(data)
            print("🗑️ Deleted!")
        else:
            print("❌ Invalid index")
    except:
        print("❌ Invalid input")

def set_budget():
    try:
        budget = float(input("Enter monthly budget: "))
        save_budget(budget)
        print("✅ Budget set!")
    except:
        print("❌ Invalid input")

# ---------- MAIN APP ----------

def main():
    data = load_data()

    while True:
        print("\n====== Finance Tracker ======")
        print("1. Add Expense")
        print("2. View This Month Total")
        print("3. View This Month by Category")
        print("4. View All Expenses")
        print("5. Delete Expense")
        print("6. Set Budget")
        print("7. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_expense(data)
        elif choice == "2":
            view_total(data)
        elif choice == "3":
            view_by_category(data)
        elif choice == "4":
            view_all(data)
        elif choice == "5":
            delete_expense(data)
        elif choice == "6":
            set_budget()
        elif choice == "7":
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()