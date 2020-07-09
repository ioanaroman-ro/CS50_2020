#include <cs50.h>
#include <stdio.h>

int main(void)
{
   int height = get_int("How high would you like Mario to jump?\n");
   do {
       if (height<1) {
      printf("That's too low! \n");
      height = get_int("How high would you like Mario to jump?\n");
   }
   else {
      if (height>8) {
      printf("That's too high! \n");
    height = get_int("How high would you like Mario to jump?\n");
      }
   }
   }
  while (height<1 || height>8);
   int i, j, spaces = 0;
   for (i = 1; i <= height; i++) {
      for (spaces = 1; spaces <= height - i; spaces++) {
         printf(" ");
      }
      for (j = 1; j <= i; j++) {
         printf("#");
      }
      printf("\n");
   }
 }