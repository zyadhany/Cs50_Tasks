#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // TODO
    string S = get_string("Message: ");

    //take every char one bu one
    for (int i = 0; S[i] != 0; i++)
    {
        //our binary num
        bool X[8] = {0};
        for (int j = 0; j < 8; j++)
        {
            X[j] = S[i] % 2;
            S[i] /= 2;
        }

        //print bulbs of binary num
        for (int j = 7; j >= 0; j--)
        {
            print_bulb(X[j]);
        }

        //print line for another char
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
