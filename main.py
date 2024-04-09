import budget_manager
import table


if __name__=="__main__":
    manager = budget_manager.BudgetManager()
    manager.set_monthly_income()

    while True:
        table.menu()
        
        menu_choice = input("Select option (1/2/3/4): ")

        if menu_choice == '1':
            print("\nPossible categories: \n1)---Housing---\n2)---Transportation---\n3)---Food---\n4)---Utilities---\n5)---Clothing---\n6)---Medical/Healthcare---\n7)---Debt---\n8)---Entertainment---\n9)---Other---")
            category_choice = input("Specify the category of expense: ")
            category_tup = {'1':'Housing', '2':'Transportation', '3':'Food', '4':'Utilities', '5':'Clothing', '6':'Medical/Healthcare', '7':'Debt', '8':'Entertainment', '9':'Other'}
            category = category_tup.get(category_choice)
            if category:
                amount = float(input("Specify the amount of expense: "))
                manager.add_expense(category, amount)
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
        else:
            print("Incorrect selection. Try again.")
