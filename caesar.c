#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    bool correct = 1;
    // checking for more than one argument
    if (argc != 2)
    {
        correct = 0;
    }
    //checking for alphanumeric characters
    else
    {
        for (int i = 0; i <= strlen(argv[1]); i++)
        {
            if (isalpha(argv[1][i]))
            {
                correct = 0;
            }
        }
    }
    //printing key error message
    if (correct == 0)
    {
        printf("Usage: ./caesar key\n");
    }
    //transforming argument from string to int
    int k = atoi(argv[1]);
    //getting user text
    string user_text = get_string("plaintext:  ");
    printf("ciphertext: ");
    //printing ciphertext
    for (int j = 0; j <= strlen(user_text); j++)
    {
        if (islower(user_text[j]))
        {
            printf("%c", ((user_text[j] - 'a' + k) % 26 + 'a'));
        }
        else
        {
            if (isupper(user_text[j]))
            {
                printf("%c", ((user_text[j] - 'A' + k) % 26 + 'A'));
            }
            else
            {
                printf("%c", user_text[j]);
            }
        }
    }
    printf("\n");
}