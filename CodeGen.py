print(" Password Generator")

import secrets
import string

def generate_random_password(length=12):
    characters = string.ascii_uppercase + string.digits
    random_password = ''.join(secrets.choice(characters) for _ in range(length))
    return random_password
pass_1 = '12345'
pass_2 = '00000'
p_code = input("Enter the password: ")
password = generate_random_password(12)
if p_code == pass_1:
  print(f"Use the secret code: {password} for next step.")
elif p_code == pass_2:
  print(f"Use {password} as your password.")
else:
  print("Invalid password. Retry again.")
while True:
  break
verify = input("Enter verification code: ")

if verify == password:
  print("Verified!")
else:
  print("Invalid password. Retry again.")
        