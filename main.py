import random
from datetime import datetime
import re


def menu():
    """
    Function to display the menu of options for the bank account management system.

    Returns:
    - int: The choice selected by the user.

    """
    print("Please enter one of the options (1 to 8):")
    print("1. Create account")
    print("2. Deposit money")
    print("3. Withdraw money")
    print("4. Check Balance in account")
    print("5. Close account")
    print("6. Display all accounts holder list")
    print("7. Total Balance in the Bank")
    print("8. Quit")

    # Validate user input
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice < 1 or choice > 8:
                print("Invalid choice, please enter a valid choice")
                continue
            return choice
        except ValueError:
            print("Invalid choice, please enter a valid choice")


def account_create(accounts):
    """
    Function to create a new bank account.

    Args:
        accounts: dict: Dictionary representing the existing database of customers.

    Returns:
        None
    """
    print("Creating a new account:")
    while True:
        # Validate ID number and check if it is a positive integer of 9 digits
        while True:
            id_number = input("Enter your ID number: ")
            if not id_number.isdigit():
                print("Error: ID number must be an integer.")
                continue
            if len(id_number) < 9:
                print("Error: ID number must be only 9 digits.")
                continue
            break

        # Check if ID number already exists in the database
        if any(account['id_number'] == id_number for account in accounts.values()):
            print("Error: ID number already exists in the bank's customer database.")
            continue

        # Validate first name and last name and check if they are not empty strings
        while True:
            first_name = input("Enter your first name: ")
            if not first_name:
                print("Error: First name cannot be empty.")
                continue
            # Check if first name contains numbers
            if not first_name.isalpha():
                print("Error: First name cannot contain numbers.")
                continue
            break

        # Validate last name and check if it is not an empty string and does not contain numbers
        while True:
            last_name = input("Enter your last name: ")
            if not last_name:
                print("Error: Last name cannot be empty.")
                continue
            if not last_name.isalpha():
                print("Error: Last name cannot contain numbers.")
                continue
            break

        # Validate date of birth and check if age is lower than 16 years and if it is a valid date
        while True:
            date_of_birth = input("Enter your date of birth (DD/MM/YYYY): ")
            try:
                date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y")
                if datetime.now().year - date_of_birth.year < 16:
                    print("Error: You must be at least 16 years old to open a bank account.")
                    continue
                break
            except ValueError:
                print("Error: Invalid date format. Please enter the date in the format DD/MM/YYYY.")

        # Validate email address and check if it already exists in the database and ends with .com OR .COM
        while True:
            email = input("Enter your email address: ")
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Error: Invalid email address.")
                continue
            if any(account['email'] == email for account in accounts.values()):
                print("Error: Email address already exists in the bank's customer database.")
                continue
            if not email.endswith(".com") and not email.endswith(".COM"):
                print("Error: Email address must end with .com or .COM.")
                continue
            break

        # Generating a new account number
        account_number = generate_account_number()

        # Check if account number already exists in the database if it does, generate a new account number
        while account_number in accounts:
            account_number = generate_account_number()

        # Add the new account to the database
        accounts[account_number] = {
            'id_number': id_number,
            'first_name': first_name.capitalize(),
            'last_name': last_name.capitalize(),
            'date_of_birth': date_of_birth,
            'email': email,
            'balance': 0  # Initializing balance to 0
        }

        # Displaying account information
        print("----------------------------- ")
        print("Account created successfully with account number:", account_number)
        print("Name:", first_name.capitalize(), last_name.capitalize())
        print("ID:", id_number)
        print("Date of birth:", date_of_birth.strftime("%d/%m/%Y"))
        print("Email:", email)
        print("Please remember your account number for future reference.")
        print("-----------------------------")
        break


def generate_account_number():
    """
    Function to generate a random 4-digit account number.

    Returns:
    - str: A string representing the generated account number.
    """
    # Generating a random 4-digit account number from 0 to 9999
    return str(random.randint(1000, 9999))


def money_deposit(accounts):
    """
    Function to deposit money into a bank account.

    Parameters:
    - database (dict): Dictionary representing the existing database of customers.

    Returns:
    - database (dict): Updated dictionary representing the database of customers.

    """
    if not accounts:
        print("There are no customers in the bank.")
        return accounts

    account_number = input("Enter the account number to deposit money into: ")
    # Check if the account number exists in the database
    if account_number not in accounts:
        print("Account not found in the bank's customer database.")
        return accounts

    amount = float(input("Enter the amount of money to deposit: "))
    # Check if the amount is positive
    if amount <= 0:
        print("Invalid amount. Please enter a positive value.")
        return accounts
    # Update account balance with the deposited amount and display the updated balance and account information
    accounts[account_number]['balance'] += amount

    print("Deposit successful.")
    print("Account number:", account_number)
    print("ID:", accounts[account_number]['id_number'])
    print("Updated balance:", accounts[account_number]['balance'], "NIS")
    # Return the updated information from the database
    return accounts


def authenticate_user(accounts, account_number):
    """
    Helper function to authenticate the user based on their details against the database.

    Parameters:
    - database (dict): Dictionary representing the existing database of customers.
    - account_number (str): The account number of the user to authenticate.

    Returns:
    - bool: True if authentication succeeds, False otherwise.
    """
    # Check if the account number exists in the database
    if account_number not in accounts:
        print("Account not found in the bank's customer database.")
        return False

    # Validate the user's ID number and validate date of birth
    id_number = input("Enter your ID number: ")
    if id_number != accounts[account_number]['id_number']:
        print("Invalid ID number.")
        return False

    date_of_birth = input("Enter your date of birth (DD/MM/YYYY): ")
    try:
        date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y")
        if date_of_birth != accounts[account_number]['date_of_birth']:
            print("Invalid date of birth.")
            return False
    except ValueError:
        print("Invalid date format. Please enter the date in the format DD/MM/YYYY.")
        return False

    print("User authentication successful.")
    return True


def money_withdraw(accounts):
    """
    Function to withdraw money from a bank account.

    Parameters:
    - database (dict): Dictionary representing the existing database of customers.

    Returns:
    - database (dict): Updated dictionary representing the database of customers.
    """

    if not accounts:
        print("There are no customers in the bank.")
        return accounts

    account_number = input("Enter the account number to withdraw money from: ")

    # Check if user authentication succeeds
    if not authenticate_user(accounts, account_number):
        print("Money cannot be withdrawn from the account because customer verification failed.")
        return accounts

    amount = float(input("Enter the amount of money to withdraw: "))

    if amount <= 0:
        print("Invalid amount. Please enter a positive value.")
        return accounts

    # Check if withdrawal amount exceeds the limit
    if accounts[account_number]['balance'] - amount < -1000:
        print("Withdrawal amount exceeds the limit. Money cannot be withdrawn from the account.")
        return accounts

    # Update account balance
    accounts[account_number]['balance'] -= amount

    print("Withdrawal successful.")
    print("Account number:", account_number)
    print("ID:", accounts[account_number]['id_number'])
    print("Updated balance:", accounts[account_number]['balance'], "NIS")

    return accounts


def balance_check(accounts):
    """
    Function to check the balance of a bank account.

    Parameters:
    - database (dict): Dictionary representing the existing database of customers.

    Returns:
    - None
    """
    if not accounts:
        print("There are no customers in the bank.")
        return

    account_number = input("Enter the account number to check balance: ")

    if account_number not in accounts:
        print("Account not found in the bank's customer database.")
        return

    account_info = accounts[account_number]
    print("Account number:", account_number)
    print("Name:", account_info['first_name'], account_info['last_name'])
    print("ID:", account_info['id_number'])
    print("Date of birth:", account_info['date_of_birth'].strftime("%d/%m/%Y"))
    print("Email:", account_info['email'])
    print("Balance:", account_info['balance'], "NIS")


def account_close(accounts):
    """
    Function to close a bank account.

    Parameters:
    - accounts (dict): Dictionary representing the existing database of customers.

    Returns:
    - accounts (dict): Updated dictionary representing the database of customers.
    """

    if not accounts:
        print("There are no customers in the bank.")
        return accounts

    account_number = input("Enter the account number to close: ")

    if account_number not in accounts:
        print("Account not found in the bank's customer database.")
        return accounts

    # Check if user authentication succeeds
    if not authenticate_user(accounts, account_number):
        print("Bank account cannot be closed because customer identification has failed.")
        return accounts

    # Check if the account has a positive balance and refunding the balance to the customer
    balance = accounts[account_number]['balance']
    if balance > 0:
        print(f"You have a balance of {balance} in your account.")
        print("Your account will be closed and the balance will be refunded.")
        print("Please wait while we process your request...")
        print("Refunding the balance to the customer...")
        print(f"Balance of {balance} refunded successfully.")

    # Closing the account and remove it from the database
    del accounts[account_number]
    print("Account closed successfully.")
    return accounts


def display_all_accounts(accounts):
    """
    Function to display all accounts in the bank.

    Parameters:
    - database (dict): Dictionary representing the existing database of customers.

    Returns:
    - None
    """

    # Check if there are no accounts in the bank
    if not accounts:
        print("There are no customers in the bank.")
        return
    # Print total number of accounts in the bank and display all accounts
    print(f"Total number of accounts in the bank: {len(accounts)}")
    print("List of all accounts in the bank:")
    for account_number, account_info in accounts.items():
        print("Account number:", account_number)
        print("Name:", account_info['first_name'], account_info['last_name'])
        print("Balance:", account_info['balance'], "NIS")
        print("-----------------------------")
        print()  # Empty line for better readability


def total_bank_balance(accounts):
    """
    Function to calculate and print the total balances in the bank.

    Parameters:
    - database (dict): Dictionary representing the existing database of customers.

    Returns:
    - None
    """

    # Calculating the total balance in the bank and display it to the user
    total_balance = sum(account_info['balance'] for account_info in accounts.values())
    print("Total balance in the bank:", total_balance, "NIS")


def main():
    """
    Main function to run the bank account management system.
    Returns:
    - None
    """
    # Creating an empty dictionary to store the bank accounts information (account number as key and account details
    # as value)
    accounts = {}
    while True:
        # Display the menu and get the choice from the user
        choice = menu()
        # Use the user's choice to call the appropriate function
        match choice:
            case 1:
                # Create account
                account_create(accounts)
            case 2:
                # Deposit money
                money_deposit(accounts)
            case 3:
                # Withdraw money
                money_withdraw(accounts)
            case 4:
                # Check balance
                balance_check(accounts)
            case 5:
                # Close account
                account_close(accounts)
            case 6:
                # Display all accounts
                display_all_accounts(accounts)
            case 7:
                # Total balance in the bank
                total_bank_balance(accounts)
            case 8:
                print("Thank you for using the bank account management system. Goodbye!")
                break
            case _:
                # Invalid choice entered by the user
                print("Invalid choice, please enter a valid choice")


# Run the main function


if __name__ == '__main__':
    main()