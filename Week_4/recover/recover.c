#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint8_t BYTE;
const int BLOCK_SIZE = 512 * sizeof(BYTE);

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return (1);
    }

    int x = 0;

    FILE* file = fopen(argv[1], "r");
    FILE* img;

    char * file_name = argv[1];
    BYTE buffer[512];
    char name[8] = {0};

    while (fread(buffer, sizeof(BYTE) * 512, 1, file) == 1)
    {

        if (buffer[0] == 0xFF && buffer[1] == 0xD8 && buffer[2] == 0xFF && (buffer[3] & 0xF0) == 0xE0)
        {

            if (img != NULL)
            {
                fclose(img);
            }
            sprintf(name, "%03d.jpg", x++);

            img = fopen(name, "w");
        }


        if (img != NULL)
        {
            fwrite(buffer, sizeof(BYTE) * 512, 1, img);
        }
    }

    fclose(file);

}