import sys
import csv


def main():
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit()

    # Rename arguments
    database = sys.argv[1]
    sequences = sys.argv[2]

    # Create list of database persons
    people = []
    with open(database, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            people.append(row)

    # Create a list for item in dna sequence
    with open(sequences, 'r') as txtfile:
        lines = [l.rstrip("\n") for l in txtfile]

    # Create a list for strings to search
    header = people[0]
    strings = []
    for entry in header:
        strings.append(entry)
    del strings[0]

    maximum = []

    # Search for repetition
    for i in range(len(strings)):
        key = strings[i]
        count = 0
        countMax = 0
        copy = lines
        index = index1 = copy[0].find(key)

        # Search for dna string based on index
        while copy[0][index:index+len(key)] == key:
            if index == index1:
                count += 1
                copy[0] = copy[0][:index1] + copy[0][(index1+len(key)):]
                index = copy[0].find(key)
                if count > countMax:
                    countMax = count
            else:
                # Move the index to the next group
                index1 = index
                count = 0

        # Create list to store maximum values
        maximum.append(countMax)

    for person in people:
        match = 0
        # compares the sequences to every person and prints name before leaving the program if there is a match
        for i in range(len(maximum)):
            if maximum[i] == int(person[strings[i]]):
                match += 1

        if match == len(maximum):
            print(person['name'])
            exit()

    print("No match")


main()