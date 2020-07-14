#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main (void) {
float change = 0;
do
{
   change = get_float("How much change are you owed?\n");
}
while (change<0);
int cents = round (change * 100);
int i = 0;
int a = round (cents/25);
cents = cents - a*25;
int b = round (cents/10);
cents = cents - b*10;
int c = round (cents/5);
cents = cents - c*5;
int coins = a+b+c+cents;
printf("%i \n", coins);
}