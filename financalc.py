
# Simple Financial Calculation

budget = input("Enter your budget: ")

try:
    budget_value = float(budget.replace(",", "").replace("₹", "").strip())

    if budget_value <= 0:
        print("\nBudget must be greater than zero.")

    else:
        inventory = budget_value * 0.40
        operations = budget_value * 0.30
        marketing = budget_value * 0.10
        emergency = budget_value * 0.20

        print("\nSUGGESTED BUDGET ALLOCATION")
        print("-" * 40)
        print(f"Inventory / Product: ₹{inventory:,.2f}")
        print(f"Operations: ₹{operations:,.2f}")
        print(f"Marketing: ₹{marketing:,.2f}")
        print(f"Emergency Reserve: ₹{emergency:,.2f}")
        print("-" * 40)
        print(f"Total Budget: ₹{budget_value:,.2f}")

except ValueError:
    print("\nInvalid budget. Please enter a valid number.")
