from datetime import datetime 
import secrets
import string
import random


def generate_random_code(length=10):
    characters = string.ascii_uppercase
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code  

def display_menu():
    
    print("1. M-Pesa")

def mpesa_service():
    print("1. Send Money")
    print("2. Withdraw Money")

    select = input("Select choice: ")
    if select == "1":
        user = input("Enter amount to send: ")
        phone = random.randint(700000000, 1111111111)
        confirm_transaction(user, phone)
    elif select == "2":
        user = input("Enter amount to withdraw: ")
        confirm_withdrawal(user)
    else:
        print("Invalid input. Select 1 or 2.")

def confirm_transaction(amount, phone):
    code = generate_random_code()
    balance = random.randint(999, 99999)
    time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    
    print("Do you want to send money 💰?")
    print("1. Yes.")
    print("2. No.")
    option = input("Select: ")
    if option == "1":
        print(f"{code} Confirmed. KES {amount} sent to {phone}. New MPESA balance is KES {balance} \n on {time}.")
    else:
        print("Transaction cancelled.")

def confirm_withdrawal(amount):
    code = generate_random_code()
    balance = random.randint(999, 99999)
    time = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    print(f"{code} Confirmed. You've withdrawn \n KES {amount}. Your current balance is KES {balance} \n at {time}")

while True:
    print("M-Pesa Services:")
    mpesa_service()
    break 

    