#include <cs50.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include <stdio.h>

float get_letters(string phrase);
float get_words(string phrase);
float get_sentences(string phrase);
float get_index(float let, float wo, float sen);

int main(void)
{
    // Getting user input text
    string phrase = get_string("Text: \n");
    //Counting letters
    float let = get_letters(phrase);
    //Counting words
    float wo = get_words(phrase);
    //Counting sentences
    float sen = get_sentences(phrase);
    //Calculating the Coleman-Liau index
    float ind = get_index(let, wo, sen);
    //Returning the grade
    if (ind < 1)
    {
        printf("Before grade 1 \n");
    }
    else
    {
        if (ind > 16)
        {
            printf("Grade 16+ \n");
        }
        else
        {
            printf("Grade: %.0f \n", ind);
        }
    }
}

float get_letters(string phrase)
{
    int letters = 0;
    for (int i = 0; i <= strlen(phrase); i++)
    {
        if (isalpha(phrase[i]))
        {
            letters++;
        }
    }
    return letters;
}
float get_words(string phrase)
{
    int words = 0;
    for (int j=0; j <= strlen(phrase);j++)
    {
            if (phrase[j]==' ' || phrase[j] == '\0')
            {
                words++;
            }
    }
    return words;
}
float get_sentences(string phrase)
{
    int sentences = 0;
    for (int k = 0; k <= strlen(phrase); k++)
    {
        if (phrase[k] == '.' || phrase[k] == '!' || phrase[k] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}
float get_index(float let, float wo, float sen)
{
    float index = 0;
    double L = 0;
    double S = 0;
    L = let / wo * 100;
    S = sen / wo * 100;
    index = round(0.0588 * L - 0.296 * S - 15.8);
    return index;
}