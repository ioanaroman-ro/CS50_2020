#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int a = round(((float)image[i][j].rgbtRed + (float)image[i][j].rgbtGreen + (float)image[i][j].rgbtBlue)/3);
            image[i][j].rgbtRed = a;
            image[i][j].rgbtGreen = a;
            image[i][j].rgbtBlue = a;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int nr = 0;
    int ng = 0;
    int nb = 0;
    for (int i = 0; i < (height - 1); i++)
    {
        for (int j = 0; j < (width - 1); j++)
        {
            nr = round((float)image[i][j].rgbtRed * 0.393 + (float)image[i][j].rgbtGreen * 0.769 + (float)image[i][j].rgbtBlue * 0.189);
            ng = round((float)image[i][j].rgbtRed * 0.349 + (float)image[i][j].rgbtGreen * 0.686 + (float)image[i][j].rgbtBlue * 0.168);
            nb = round((float)image[i][j].rgbtRed * 0.272 + (float)image[i][j].rgbtGreen * 0.534 + (float)image[i][j].rgbtBlue * 0.131);
            if (nr < 255)
            {
                image[i][j].rgbtRed = nr;
            }
            else
            {
                image[i][j].rgbtRed = 255;
            }
            if (ng < 255)
            {
                image[i][j].rgbtGreen = ng;
            }
            else
            {
                image[i][j].rgbtGreen = 255;
            }
            if (nb < 255)
            {
                image[i][j].rgbtBlue = nb;
            }
            else
            {
                image[i][j].rgbtBlue = 255;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
