import random
name = input("Player 1 enter your Name: ")

score = random.randint(99,999)
if score > 500:
    print("You win! You scored:", score)
else:
    print("Game over! You scored:", score)
