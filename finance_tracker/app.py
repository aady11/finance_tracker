import streamlit as st
import json
import os
from datetime import datetime

EXPENSE_FILE = "expenses.json"
BUDGET_FILE = "budget.json"

# ---------- DATA ----------

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
        with open(BUDGET_FILE, "r") as file:
            return json.load(file).get("budget", 0)
    return 0

def save_budget(budget):
    with open(BUDGET_FILE, "w") as file:
        json.dump({"budget": budget}, file)

# ---------- UI ----------

st.set_page_config(page_title="Finance Tracker", layout="centered")

st.title("💸 Personal Finance Tracker")

data = load_data()

# ---------- ADD EXPENSE ----------

st.subheader("➕ Add Expense")

amount = st.number_input("Amount", min_value=0.0, step=1.0)
category = st.text_input("Category")

if st.button("Add Expense"):
    if category:
        expense = {
            "amount": amount,
            "category": category.lower(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        data.append(expense)
        save_data(data)
        st.success("Expense added!")
    else:
        st.error("Enter category")

# ---------- BUDGET ----------

st.subheader("🎯 Set Monthly Budget")

budget_input = st.number_input("Budget", min_value=0.0, step=100.0)

if st.button("Set Budget"):
    save_budget(budget_input)
    st.success("Budget saved!")

budget = load_budget()

# ---------- CALCULATIONS ----------

current_month = datetime.now().strftime("%Y-%m")

monthly_expenses = [
    item for item in data
    if "date" in item and item["date"].startswith(current_month)
]

total = sum(item["amount"] for item in monthly_expenses)

st.subheader("💰 This Month Summary")

st.write(f"Total Spending: {total}")

if budget > 0:
    st.write(f"Budget: {budget}")
    if total > budget:
        st.error("⚠️ Budget exceeded!")
    else:
        st.success(f"Remaining: {budget - total}")

# ---------- CATEGORY BREAKDOWN ----------

st.subheader("📊 Category Breakdown")

category_data = {}

for item in monthly_expenses:
    cat = item.get("category", "unknown")
    category_data[cat] = category_data.get(cat, 0) + item["amount"]

st.bar_chart(category_data)

# ---------- ALL EXPENSES ----------

st.subheader("📋 All Expenses")

st.write(data)