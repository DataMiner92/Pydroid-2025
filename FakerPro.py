from faker import Faker

fake = Faker()

fake_date = fake.date()

fake_address = fake.address()

fake_first_name = fake.first_name()

fake_last_name = fake.last_name()

print("Date:", fake_date)

print("----------------------------------------")
print("Address:", fake_address)
print("----------------------------------------")
print("First Name:", fake_first_name)
print("Last Name:", fake_last_name)