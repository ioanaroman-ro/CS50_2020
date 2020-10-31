# TODO
import sys
import csv
from cs50 import SQL


def main():
    # Check for correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python roster.py Housename")
        sys.exit()

    # Rename arguments
    house = sys.argv[1].lower()

    # Making sure that argument is a house
    if house.lower() not in ["slytherin", "gryffindor", "ravenclaw", "hufflepuff"]:
        print("Provide house name: Gryffindor, Hufflepuff, Slytherin or Ravenclaw.")
        sys.exit()

    # Read database
    open("students.db", "r").close()
    db = SQL("sqlite:///students.db")

    query = []
    query = db.execute("SELECT first,middle,last,birth FROM students WHERE lower(house) = ? ORDER BY last, first", house)

    #Printing answer to user
    for row in query:
        if row["middle"] == None:
            print("{} {}, born {}".format(row["first"], row["last"], row["birth"]))
        else:
            print("{} {} {}, born {}".format(row["first"], row["middle"], row["last"], row["birth"]))


main()