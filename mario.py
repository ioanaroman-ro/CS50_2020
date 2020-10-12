from cs50 import get_int

#get user height
height = get_int("Height: \n")
i = 0

#check user height between 1 and 8 inclusive
while height < 1 or height > 8:
    height = get_int("Height: \n")

#print pyramid
while i < height:
    i += 1
    print(" " * (height - i) + "#" * i + "  ", end = "")
    print("#" * i, end = "")
    print()