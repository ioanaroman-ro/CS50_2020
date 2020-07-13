#include <cs50.h>
#include <stdio.h>

int correct(int height);
int main(void)
{
    //Get pyramid height
    int height = get_int("How high would you like Mario to jump?\n");
    //Check pyramid height limits
    if (correct(height)) {
    //Print pyramid
    int i, j, spaces = 0;
    for (i = 1; i <= height; i++)
    {
        for (spaces = 1; spaces <= height - i; spaces++)
        {
        printf(" ");
        }
        for (j = 1; j <= i; j++)
        {
        printf("#");
        }
        printf(" ");
        for (j = i; j >=1 ; j--)
        {
        printf("#");
        }
        printf("\n");
   }
    }

}
int correct(height)
   {
       do{
          if (height < 1)
       {
         printf("That's too low! \n");
         height = get_int("How high would you like Mario to jump?\n");
       }
       else
       {
          if (height > 8)
          {
            printf("That's too high! \n");
            height = get_int("How high would you like Mario to jump?\n");
          }
       }
       }
       while (height < 1 || height > 8);
       return 1;
              }
