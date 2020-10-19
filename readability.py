from cs50 import get_string
import re


def main():
    # User input
    phrase = get_string("Text: ")
    let = get_letters(phrase)
    wo = get_words(phrase)
    sen = get_sentences(phrase)
    ind = get_index(let, wo, sen)

    # Returning the grade
    if ind < 1:
        print("Before Grade 1")

    else:
        if ind > 16:
            print("Grade 16+")
        else:
            print("Grade ", ind)


# Counting letters

def get_letters(phrase):
    letters = 0
    digits = 0
    others = 0
    for i in phrase:
        if i.isalpha():
            letters += 1
    return letters


# Counting words

def get_words(phrase):
    words_list = phrase.split(" ")
    words = len(words_list)
    return words


# Counting sentences

def get_sentences(phrase):
    sentences = 0
    k = 0
    for k in range(len(phrase)):
        if phrase[k] in [".", "!", "?"]:
            sentences += 1
        k += 1
    return sentences


# Calculating the Coleman-Liau index

def get_index(let, wo, sen):
    # index = 0
    # L = 0
    # S = 0
    L = let / wo * 100
    S = sen / wo * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)
    return index


main()