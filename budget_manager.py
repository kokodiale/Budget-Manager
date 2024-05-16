from rich import print
import pandas as pd
from rich.prompt import Prompt, FloatPrompt

class BudgetManager:
    def __init__(self):
        self.wallet = 0
        self.monthly_income = 0
        self.expenses = {
            'Housing': 0,
            'Transportation': 0,
            'Food': 0,
            'Utilities': 0,
            'Clothing': 0,
            'Medical/Healthcare': 0,
            'Debt': 0,
            'Entertainment': 0,
            'Other': 0,
        }
        self.currency = "PLN"  # default currency
        self.conversion_rates = {
            'PLN': 1,
            'USD': 0.26,
            'EUR': 0.22,
            'JPY': 28.86
        }
    def export_to_excel(self, filename="budget.xlsx"):
        data = {
            "Category": list(self.expenses.keys()),
            "Amount": list(self.expenses.values())
        }
        df = pd.DataFrame(data)
        df.loc[len(df.index)] = ["Monthly Income", self.monthly_income]
        df.loc[len(df.index)] = ["Wallet", self.wallet]
        df.to_excel(filename, index=False)
        print(f"Data succesfully exported to {filename}")

    def set_monthly_income(self):
        self.monthly_income = FloatPrompt.ask("Specify your monthly income: ")                 # float(input("Specify your monthly income: "))
        self.wallet = self.monthly_income
        self.currency = user_currency()

    def add_expense(self, category, amount, currency):
        converted_amount = self.convert_to_pln(amount, currency)
        if category in self.expenses:
            if converted_amount <= self.wallet:
                self.expenses[category] += converted_amount
                self.wallet -= converted_amount
                print(f'Added {amount} {currency} to "{category}".')
            else:
                print("You do not have enough resources.")
        else:
            print("Wrong category.")

    def show_budget(self):
        print(f"\nMonthly income: {self.monthly_income} {self.currency}")
        print(f"Wallet: {self.wallet} {self.currency}")
        print("\nExpense categories:")
        for category, amount in self.expenses.items():
            print(f"{category}: {amount} {self.currency}")

    def total_expenses(self):
        total_expenses = sum(self.expenses.values())
        return total_expenses

    def calculate_balance(self):
        total_expenses_pln = self.total_expenses()
        balance = self.convert_to_currency(self.monthly_income - total_expenses_pln, self.currency)
        return balance

    def convert_to_pln(self, amount, currency):
        if currency == 'PLN':
            return amount
        elif currency in self.conversion_rates:
            return amount * self.conversion_rates[currency]
        else:
            print("Currency not supported for conversion. Assuming PLN.")
            return amount

    def convert_to_currency(self, amount, target_currency):
        if target_currency == 'PLN':
            return amount
        elif target_currency in self.conversion_rates:
            return amount / self.conversion_rates[target_currency]
        else:
            print("Currency not supported for conversion. Assuming PLN.")
            return amount


def user_currency():
    print("\n--- Currency ---")
    print("1. PLN")
    print("2. USD")
    print("3. EUR")
    print("4. JPY")
    print("5. other")

    currency_choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5"])                 # input("Select option (1/2/3/4/5): ")

    if currency_choice == '1':
        return "PLN"
    elif currency_choice == '2':
        return "USD"
    elif currency_choice == '3':
        return "EUR"
    elif currency_choice == '4':
        return "JPY"
    elif currency_choice == '5':
        other_currency = Prompt.ask("Enter the abbreviation of your own currency: ")                      #input("Enter the abbreviation of your own currency: ")
        return other_currency.upper()
    else:
        print("Incorrect selection. Try again.")
        return user_currency()


if __name__ == "__main__":
    manager = BudgetManager()
    manager.set_monthly_income()

    while True:
        print("\n--- Menu ---")
        print("1. Add expense")
        print("2. View budget")
        print("3. View balance")
        print("4. Finish")
        print("5. Export to Excel")

        menu_choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5"])       #input("Select option (1/2/3/4/5): ")

#printa zamienic na print z category_tup(zrobione ':)' )
        if menu_choice == '1':
            # print("\nPossible categories: \n1)---Housing---\n2)---Transportation---\n3)---Food---\n4)---Utilities---\n5)---Clothing---\n6)---Medical/Healthcare---\n7)---Debt---\n8)---Entertainment---\n9)---Other---")
            category_tup = {'1': 'Housing', '2': 'Transportation', '3': 'Food', '4': 'Utilities', '5': 'Clothing',
                            '6': 'Medical/Healthcare', '7': 'Debt', '8': 'Entertainment', '9': 'Other'}
            for i in category_tup:
                print(f"{i}) --{category_tup[i]}--")
            category_choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])                       # input("Specify the category of expense: ")
            category = category_tup.get(category_choice)
            if category:
                amount = FloatPrompt.ask("Specify the amount of expense: ")                                    # float(input("Specify the amount of expense: "))
                currency = Prompt.ask("Specify the currency of the expense: ")                               # input("Specify the currency of the expense: ")
                manager.add_expense(category, amount, currency)
            else:
                print("Incorrect category section. Try again")
        elif menu_choice == '2':
            manager.show_budget()
        elif menu_choice == '3':
            balance = manager.calculate_balance()
            total_expenses = manager.total_expenses()
            print(f"Current balance: {balance} {manager.currency} \nTotal expenses this month: {total_expenses}")
        elif menu_choice == '4':
            print("Thank you for using the app")
            break
        elif menu_choice == '5':
            filename = Prompt.ask("Enter the filename (with .xlsx extension): ", default="budget.xlsx")                                 # input("Enter the filename (with .xlsx extension): ")
            manager.export_to_excel(filename)
        else:
            print("Incorrect selection. Try again.")
