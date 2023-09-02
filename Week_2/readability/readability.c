#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    //my var
    double n, l = 0, s = 0, w = 1;

    //take string
    string S = get_string("Text: ");

    //cout l and s and w
    for (int i = 0; S[i] != 0; i++)
    {
        if (S[i] == ' ')
        {
            //increase word
            w++;
        }
        else if (S[i] == '!' || S[i] == '.' || S[i] == '?')
        {
            //increase sentecs
            s++;
        }
        else if (islower(S[i]) || isupper(S[i]))
        {
            l++;
        }
    }

    //calculate L and S
    l = (l / w) * 100;
    s = (s / w) * 100;

    //get grade
    l = 0.0588 * l - 0.296 * s - 15.8;
    int grade = l;
    grade += (l >= grade + 0.5);
    if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %d\n", grade);
    }
}