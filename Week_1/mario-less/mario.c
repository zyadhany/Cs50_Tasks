//libraries
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //taking input
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n <= 0 || n > 8);


    //drawin stage
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (j >= n - i - 1)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("\n");
    }
}