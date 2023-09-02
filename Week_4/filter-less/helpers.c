#include "helpers.h"
#include <stdio.h>
#include <math.h>

//color i want tto play around
RGBTRIPLE k;

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    //loop for all element of array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //the gray scale
            int g = 0;
            g += image[i][j].rgbtBlue;
            g += image[i][j].rgbtRed;
            g += image[i][j].rgbtGreen;
            g = (g + 1) / 3;

            //give the pixel color
            k.rgbtRed = g;
            k.rgbtGreen = g;
            k.rgbtBlue = g;
            image[i][j] = k;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //loop for all element of array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //get orignal
            double originalBlue = image[i][j].rgbtBlue;
            double originalRed = image[i][j].rgbtRed;
            double originalGreen = image[i][j].rgbtGreen;
            //make it double
            double a, b, c;
            a = 0.393 * originalRed + 0.769 * originalGreen + 0.189 * originalBlue;
            b = 0.349 * originalRed + 0.686 * originalGreen + 0.168 * originalBlue;
            c = 0.272 * originalRed + 0.534 * originalGreen + 0.131 * originalBlue;
            //cap at 255 value
            if (a > 255)
            {
                a = 255;
            }
            if (b > 255)
            {
                b = 255;
            }
            if (c > 255)
            {
                c = 255;
            }
            //swap to sopia
            image[i][j].rgbtRed = round(a);
            image[i][j].rgbtGreen = round(b);
            image[i][j].rgbtBlue = round(c);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //loop for all element of array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            //swap 2 pixel
            k = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = k;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //make temp array
    RGBTRIPLE X[height][width];

    //make new array of blue
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int a = 0, b = 0, c = 0, m = 0;

            for (int l = i - 1; l <= i + 1; l++)
            {
                for (int r = j - 1; r <= j + 1; r++)
                {
                    if (l < 0 || l >= height || r < 0 || r >= width)
                    {
                        continue;
                    }
                    a += image[l][r].rgbtRed;
                    b += image[l][r].rgbtGreen;
                    c += image[l][r].rgbtBlue;
                    m++;
                }
            }

            //get Blur scale
            k.rgbtRed = (a + (m / 2)) / m;
            k.rgbtGreen = (b + (m / 2)) / m;
            k.rgbtBlue = (c + (m / 2)) / m;
            X[i][j] = k;
        }
    }


    //swap the arrays
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = X[i][j];
        }
    }
    return;
}
