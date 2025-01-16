print("Simple Calculator :")

import math
def display_menu():
    print("1. Mult.")
    print("2. Add.")
    print("3. Div.")
    print("4. Sqr.")
    print("5. Expon.")
    print ("6. Exit.")

while True:
    display_menu()
    break
choice = input("Select: ")

x = int(input("Enter first number : "))
y = int(input("Enter second number: "))
    
a = x * y
b = x + y
c =  x / y
d = y * y
e = x ** y


if choice == "1":
      print(f" The product is:  {a}")    
elif choice == "2":
 print(f"The sum is {b}") 
elif choice == "3":
    print(f"The  answer is {c}")
elif choice == "4":
    print(f" The square is {d}")
elif choice == "5":
    print(f" The exponential power is {e}")
else:
    print("Exiting ...")


