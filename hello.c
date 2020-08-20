#include <stdio.h>
#include <cs50.h>

int main(void)
{
// user has to input his/her's name
    string name = get_string("What's your name?\n");
//program greets user
    printf("hello, %s! \n", name);
}