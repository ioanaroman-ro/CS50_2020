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
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
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
    RGBTRIPLE first = image[0][0];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width/2); j++)
        {
            first = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = first;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE original[height][width];
    int w = width - 1;
    int h = height - 1;
    for (int i = 0; i < height; i++)
    {
        for ( int j = 0; j < width; j++)
        {
            original[i][j] = image[i][j];
        }
    }
    image[0][0].rgbtRed = round(((float)original[0][0].rgbtRed+(float)original[0][1].rgbtRed+(float)original[1][0].rgbtRed+(float)original[1][1].rgbtRed)/4);
    image[0][0].rgbtGreen = round(((float)original[0][0].rgbtGreen+(float)original[0][1].rgbtGreen+(float)original[1][0].rgbtGreen+(float)original[1][1].rgbtGreen)/4);
    image[0][0].rgbtBlue = round(((float)original[0][0].rgbtBlue+(float)original[0][1].rgbtBlue+(float)original[1][0].rgbtBlue+(float)original[1][1].rgbtBlue)/4);
    image[0][w].rgbtRed = round(((float)original[0][w-1].rgbtRed+(float)original[0][w].rgbtRed+(float)original[1][w-1].rgbtRed+(float)original[1][w].rgbtRed)/4);
    image[0][w].rgbtGreen = round(((float)original[0][width-1].rgbtGreen+(float)original[0][width-2].rgbtGreen+(float)original[1][width-2].rgbtGreen+(float)original[1][width-1].rgbtGreen)/4);
    image[0][w].rgbtBlue = round(((float)original[0][width-1].rgbtBlue+(float)original[0][width-2].rgbtBlue+(float)original[1][width-2].rgbtBlue+(float)original[1][width-1].rgbtBlue)/4);
    image[height-1][0].rgbtRed = round(((float)original[height-1][0].rgbtRed+(float)original[height-1][1].rgbtRed+(float)original[height-2][0].rgbtRed+(float)original[height-2][1].rgbtRed)/4);
    image[height-1][0].rgbtGreen = round(((float)original[height-1][0].rgbtGreen+(float)original[height-1][1].rgbtGreen+(float)original[height-2][0].rgbtGreen+(float)original[height-2][1].rgbtGreen)/4);
    image[height-1][0].rgbtBlue = round(((float)original[height-1][0].rgbtBlue+(float)original[height-1][1].rgbtBlue+(float)original[height-2][0].rgbtBlue+(float)original[height-2][1].rgbtBlue)/4);
    image[height-1][width-1].rgbtRed = round(((float)original[height-1][width-1].rgbtRed+(float)original[height-2][width-2].rgbtRed+(float)original[height-2][width-1].rgbtRed+(float)original[height-1][width-2].rgbtRed)/4);
    image[height-1][width-1].rgbtGreen = round(((float)original[height-1][width-1].rgbtGreen+(float)original[height-2][width-2].rgbtGreen+(float)original[height-2][width-1].rgbtGreen+(float)original[height-1][width-2].rgbtGreen)/4);
    image[height-1][width-1].rgbtBlue = round(((float)original[height-1][width-1].rgbtBlue+(float)original[height-2][width-2].rgbtBlue+(float)original[height-2][width-1].rgbtBlue+(float)original[height-1][width-2].rgbtBlue)/4);
    for (int i = 1; i < height; i++)
    {
        image[i][0].rgbtRed = round(((float)original[i-1][0].rgbtRed + (float)original[i-1][1].rgbtRed + (float)original[i][0].rgbtRed + (float)original[i][1].rgbtRed + (float)original[i+1][0].rgbtRed + (float)original[i+1][1].rgbtRed)/6);
        image[i][0].rgbtGreen = round(((float)original[i-1][0].rgbtGreen + (float)original[i-1][1].rgbtGreen + (float)original[i][0].rgbtGreen + (float)original[i][1].rgbtGreen + (float)original[i+1][0].rgbtGreen + (float)original[i+1][1].rgbtGreen)/6);
        image[i][0].rgbtBlue = round(((float)original[i-1][0].rgbtBlue + (float)original[i-1][1].rgbtBlue + (float)original[i][0].rgbtBlue + (float)original[i][1].rgbtBlue + (float)original[i+1][0].rgbtBlue + (float)original[i+1][1].rgbtBlue)/6);
    }
    for (int j = 1; j < width; j++)
    {
        image[0][j].rgbtRed = round(((float)original[0][j-1].rgbtRed + (float)original[0][j].rgbtRed + (float)original[0][j+1].rgbtRed + (float)original[1][j-1].rgbtRed + (float)original[1][j].rgbtRed + (float)original[1][j+1].rgbtRed)/6);
        image[0][j].rgbtGreen = round(((float)original[0][j-1].rgbtGreen + (float)original[0][j].rgbtGreen + (float)original[0][j+1].rgbtGreen + (float)original[1][j-1].rgbtGreen + (float)original[1][j].rgbtGreen + (float)original[1][j+1].rgbtGreen)/6);
        image[0][j].rgbtBlue = round(((float)original[0][j-1].rgbtBlue + (float)original[0][j].rgbtBlue + (float)original[0][j+1].rgbtBlue + (float)original[1][j-1].rgbtBlue + (float)original[1][j].rgbtBlue + (float)original[1][j+1].rgbtBlue)/6);
    }
    for (int i = 1; i < height; i++)
    {
        image[i][width].rgbtRed = round(((float)original[i-1][width].rgbtRed + (float)original[i-1][width-1].rgbtRed + (float)original[i][width].rgbtRed + (float)original[i][width-1].rgbtRed + (float)original[i+1][width-1].rgbtRed + (float)original[i+1][width].rgbtRed)/6);
        image[i][width].rgbtGreen = round(((float)original[i-1][width].rgbtGreen + (float)original[i-1][width-1].rgbtGreen + (float)original[i][width].rgbtGreen + (float)original[i][width-1].rgbtGreen + (float)original[i+1][width-1].rgbtGreen + (float)original[i+1][width].rgbtGreen)/6);
        image[i][width].rgbtBlue = round(((float)original[i-1][width].rgbtBlue + (float)original[i-1][width-1].rgbtBlue + (float)original[i][width].rgbtBlue + (float)original[i][width-1].rgbtBlue + (float)original[i+1][width-1].rgbtBlue + (float)original[i+1][width].rgbtBlue)/6);
    }
    for (int j = 1; j < width; j++)
    {
        image[height][j].rgbtRed = round(((float)original[height][j-1].rgbtRed + (float)original[height][j].rgbtRed + (float)original[height][j+1].rgbtRed + (float)original[height-1][j-1].rgbtRed + (float)original[height-1][j].rgbtRed + (float)original[height-1][j+1].rgbtRed)/6);
        image[height][j].rgbtGreen = round(((float)original[height][j-1].rgbtGreen + (float)original[height][j].rgbtGreen + (float)original[height][j+1].rgbtGreen + (float)original[height-1][j-1].rgbtGreen + (float)original[height-1][j].rgbtGreen + (float)original[height-1][j+1].rgbtGreen)/6);
        image[height][j].rgbtBlue = round(((float)original[height][j-1].rgbtBlue + (float)original[height][j].rgbtBlue + (float)original[height][j+1].rgbtBlue + (float)original[height-1][j-1].rgbtBlue + (float)original[height-1][j].rgbtBlue + (float)original[height-1][j+1].rgbtBlue)/6);
    }
    for (int i = 1; i < height - 1; i++)
    {
        for (int j = 1; j < width - 1; j++)
        {
            image[i][j].rgbtRed = round(((float)original[i-1][j-1].rgbtRed + (float)original[i-1][j].rgbtRed + (float)original[i-1][j+1].rgbtRed + (float)original[i][j-1].rgbtRed + (float)original[i][j].rgbtRed + (float)original[i][j+1].rgbtRed + (float)original[i+1][j-1].rgbtRed + (float)original[i+1][j].rgbtRed + (float)original[i+1][j+1].rgbtRed)/9);
            image[i][j].rgbtGreen = round(((float)original[i-1][j-1].rgbtGreen + (float)original[i-1][j].rgbtGreen + (float)original[i-1][j+1].rgbtGreen + (float)original[i][j-1].rgbtGreen + (float)original[i][j].rgbtGreen + (float)original[i][j+1].rgbtGreen + (float)original[i+1][j-1].rgbtGreen + (float)original[i+1][j].rgbtGreen + (float)original[i+1][j+1].rgbtGreen)/9);
            image[i][j].rgbtBlue = round(((float)original[i-1][j-1].rgbtBlue + (float)original[i-1][j].rgbtBlue + (float)original[i-1][j+1].rgbtBlue + (float)original[i][j-1].rgbtBlue + (float)original[i][j].rgbtBlue + (float)original[i][j+1].rgbtBlue + (float)original[i+1][j-1].rgbtBlue + (float)original[i+1][j].rgbtBlue + (float)original[i+1][j+1].rgbtBlue)/9);
        }
    }
    return;
}
