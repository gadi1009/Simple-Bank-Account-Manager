# Simple-Bank-Account-Manager(Python CLI)

A simple command-line based Bank Account Management System developed in Python.  
This project was created as an early-stage academic exercise during the first year of study and serves as a foundation for understanding user input handling, data structures, and basic program flow.

## Features

- Create new bank accounts with validation (ID, name, DOB, email)
- Deposit money into existing accounts
- Withdraw money with overdraft protection (up to -1000 NIS)
- Check individual account balance
- Close an account and refund the balance
- Display all account holders
- View total funds stored in the bank

## Technologies

- Python 3.x
- `datetime` for age verification
- `random` for generating unique account numbers
- `re` for email validation

## Disclaimer

This project is a simplified simulation of banking operations, built for learning purposes only.  
It does not include persistent storage, encryption, or security mechanisms required for production systems.

## Getting Started

To run the application:

```bash
python main.py

