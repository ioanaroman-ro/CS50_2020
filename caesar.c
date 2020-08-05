#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    bool incorrect = 0;
    // checking for more than one argument
    if (argc != 2)
    {
        incorrect = 1;
        return 1;
    }
    //checking for alphanumeric characters
    else
    {
        for (int i = 0; i <= strlen(argv[1]); i++)
        {
            if (isalpha(argv[1][i]))
            {
                incorrect = 1;
                return 1;
            }
        }
    }
    //printing key error message
    if (incorrect == 1)
    {
        printf("Usage: ./caesar key\n");
    }
    else
    {
        //transforming argument from string to int
        int k = atoi(argv[1]);
        //getting user text
        string user_text = get_string("plaintext:  ");
        printf("ciphertext: ");
        //printing ciphertext
        for (int j = 0; j <= strlen(user_text); j++)
        {
            //verifying lowercase
            if (islower(user_text[j]))
            {
                printf("%c", (((user_text[j] - 'a' + k) % 26) + 'a'));
            }
            //verifying uppercase
            else
            {
                if (isupper(user_text[j]))
                {
                    printf("%c", (((user_text[j] - 'A' + k) % 26) + 'A'));
                }
                //printing everything else
                else
                {
                    printf("%c", user_text[j]);
                }
            }
        }
        printf("\n");
        return 0;
    }
}