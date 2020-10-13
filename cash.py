from cs50 import get_float

change = get_float("Change owed: ")
# Ask user for change owed and verify
while change < 0:
    change = get_float("Change owed: ")
# Minimum number of coins possible
cents = round(change * 100)
a = cents // 25
cents = cents - a * 25
b = cents // 10
cents = cents - b * 10
c = cents // 5
cents = cents - c * 5
print(a + b + c + cents)