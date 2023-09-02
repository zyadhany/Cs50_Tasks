#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    if (argc != 3)
    {
        printf("error in argument\n");
        return 1;
    }

    // Open input file for reading
    // TODO #2
    FILE *fn = fopen(argv[1], "rb");

    if (fn == NULL)
    {
        printf("Error opening input file\n");
        return 1;
    }

    // Read header
    // TODO #3
    WAVHEADER header;

    if (fread(&header, sizeof(header), 1, fn) != 1)
    {
        printf("Error reading WAV header\n");
        return 1;
    }

    // Use check_format to ensure WAV format
    // TODO #4
    if (!check_format(header) || !header.audioFormat)
    {
        printf("Wrong format\n");
        return 1;
    }


    // Open output file for writing
    // TODO #5
    FILE *fo = fopen(argv[2], "wb");

    if (fo == NULL)
    {
        printf("Error opening output file\n");
        return 1;
    }

    // Write header to file
    // TODO #6
    if (fwrite(&header, sizeof(header), 1, fo) != 1)
    {
        printf("Error writing WAV header\n");
        return 1;
    }

    // Use get_block_size to calculate size of block
    // TODO #7
    int k = get_block_size(header);


    // Write reversed audio to file
    // TODO #8
    fseek(fn, k, SEEK_END);

    BYTE c[k];

    while (ftell(fn) - k > sizeof(header))
    {

        
        fread(c, k, 1, fn);
        fwrite(c, k, 1, fo);
    }


    //closeing files
    fclose(fn);
    fclose(fo);
}

int check_format(WAVHEADER header)
{
    char s[] = "WAVE";
    for (int i = 0; i < 4; i++)
    {
        if (header.format[i] != s[i])
        {
            return 0;
        }
    }
    return 1;
}

int get_block_size(WAVHEADER header)
{
    return (header.bitsPerSample / 8) * header.numChannels;
}