#include "helpers.h"

//take datatype of color


void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    //color i want
    RGBTRIPLE k;
    k.rgbtBlue = 123;
    k.rgbtGreen = 200;
    k.rgbtRed = 255;
    //loop for all element of array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //check if it's BLack
            if (image[i][j].rgbtBlue == 0 && image[i][j].rgbtRed == 0 && image[i][j].rgbtGreen == 0)
            {
                //change the color
                image[i][j] = k;
            }
        }
    }
}
