from rich import print
import pandas as pd
from rich.prompt import Prompt, FloatPrompt, IntPrompt
import os

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
    
    #funkcja działa zawsze po starcie kodu tóż przed poproszeniem użytkownika o dane, pozwala podjąc decyzję czy chcę on importować
    def xlsx_finder(self):
        all_files = os.listdir()
        xlsx_files = [file for file in all_files if file.endswith('.xlsx')]
        if len(xlsx_files) == 0:
            return []
        else:
            decition = Prompt.ask("The program has detected an .xlsx file, you want to import data from it" ,choices=["yes", "no"], default="no") #jeśli jest dostępny plik .xlsx ta linijka zapyta użytkownika czy chce on go zaimpotrować
            match decition:
                case "yes":
                    return xlsx_files
                case "no":
                    return []

    def set_monthly_income(self):
        xlsx_files = self.xlsx_finder()       #wstawienie wyniku funkcji sprawdzającej do obecnej
        if len(xlsx_files) == 0:              # sprawdzenie czy w obecnym folderze są pliki z rozszerzeniem .xlsx
            self.monthly_income = FloatPrompt.ask("Specify your monthly income")      
            self.wallet = self.monthly_income
            self.currency = user_currency()
        else:
            if len(xlsx_files) == 1:      
                user_file = xlsx_files[0]      #automatyczny import z pliku gdy jest dostępny tylko jeden
            else: 
                user_file = Prompt.ask("Please select a file", choices=xlsx_files)       #gdy program wykyje wiecej plików w odpowiednim formacie zapyta którego użyć
            df = pd.read_excel(user_file, sheet_name='Sheet1')                       #df to arkusz do którego się odnosimy
            self.monthly_income = df.iat[9, 1]                     #przypisanie wartości do miesięcznych wpływów z komurki o wspórzędnych [9,1][index_wiersza, index_kolumny]
            self.wallet = df.iat[10, 1]
            self.currency = user_currency()           #bez zmian
            self.expenses["Housing"] = df.iat[0, 1]
            self.expenses["Transportation"] = df.iat[1, 1]
            self.expenses["Food"] = df.iat[2, 1]
            self.expenses["Utilities"] = df.iat[3, 1]
            self.expenses["Clothing"] = df.iat[4, 1]
            self.expenses["Medical/Healthcare"] = df.iat[5, 1]
            self.expenses["Debt"] = df.iat[6, 1]
            self.expenses["Entertainment"] = df.iat[7, 1]
            self.expenses["Other"] = df.iat[8, 1]


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
    Cur_Dict = {1:"PLN", 2:"USD", 3:"EUR", 4:"JPY"}
    print("--- [blue]Currency[/blue] ---")
    for i in Cur_Dict:
                print(f"{i}. {Cur_Dict[i]}")

    currency_choice = IntPrompt.ask("Select option", choices=["1", "2", "3", "4"])       
    match currency_choice:
        case "1":
            return "PLN"
        case "2":
            return "USD"
        case "3":
            return "EUR"
        case "4":
            return "JPY"

if __name__ == "__main__":
    manager = BudgetManager()
    manager.set_monthly_income()

    while True:
        menu = {"1":"Add expense", "2":"View budget", "3":"View balance","4":"Finish", "5":"Export to Excel"}
        print("\n--- [blue]Menu[/blue] ---")
        for i in menu:
                print(f"{i}. {menu[i]}")

        menu_choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5"])

        match menu_choice:
            case "1":
                category_tup = {'1': 'Housing', '2': 'Transportation', '3': 'Food', '4': 'Utilities', '5': 'Clothing',
                                '6': 'Medical/Healthcare', '7': 'Debt', '8': 'Entertainment', '9': 'Other'}
                for i in category_tup:
                    print(f"{i}) --{category_tup[i]}--")
                category_choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])                
                category = category_tup.get(category_choice)
                if category:
                    amount = FloatPrompt.ask("Specify the amount of expense")                               
                    currency = Prompt.ask("Specify the currency of the expense")                   
                    manager.add_expense(category, amount, currency)
                else:
                    print("Incorrect category section. Try again")
            case "2":
                manager.show_budget()
            case "3":
                balance = manager.calculate_balance()
                total_expenses = manager.total_expenses()
                print(f"Current balance: {balance} {manager.currency} \nTotal expenses this month: {total_expenses}")
            case "4":
                print("Thank you for using the app")
                break
            case "5":
                filename = Prompt.ask("Enter the filename (with .xlsx extension)", default="budget.xlsx")                                
                manager.export_to_excel(filename)




# Import z pliku exel
# dynamiczne rozszerzenie listy walut przez użytkownika
# *te waluty nie były z góry definiowane tylko robione poprzez API