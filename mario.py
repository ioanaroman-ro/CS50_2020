from cs50 import get_int

height = get_int("Height: \n")

while height < 1 or height > 8:
    height = get_int("Height: \n")

i = 0

while i < height:
    i += 1
    print(" " * (height - i), end = "")
    print("#" * i, end = "")
    print()