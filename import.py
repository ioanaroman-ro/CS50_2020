# TODO
import sys
import csv
from cs50 import SQL


def main():
    # Check for correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python import.py characters.csv")
        sys.exit()

    # Rename arguments
    studentsf = sys.argv[1]

    # Making sure that argument is a *.csv file
    if not (studentsf.endswith(".csv")):
        print("You must provide a *.csv")
        sys.exit()

    # Create database
    open("students.db", "w").close()
    db = SQL("sqlite:///students.db")

    # Create table
    db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMBERIC)")

    # Open *.csv file
    with open(studentsf, "r") as file:
        reader = csv.DictReader(file)

        # Iterating rows
        for row in reader:
            # Parsing names list
            studentsl = []
            studentsl.append(row["name"].split())
            if len(studentsl[0]) == 3:
                db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES (?,?,?,?,?)",
                           studentsl[0][0], studentsl[0][1], studentsl[0][2], row["house"], int(row["birth"]))
            elif len(studentsl[0]) == 2:
                db.execute("INSERT INTO students(first, last, house, birth) VALUES (?,?,?,?)",
                           studentsl[0][0], studentsl[0][1], row["house"], int(row["birth"]))


main()