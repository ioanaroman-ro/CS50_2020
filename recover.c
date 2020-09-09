#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //Check to have exactly one argument
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    //Open original file
    FILE *init_f = fopen(argv[1], "r");
    //Check to see if it's empty
    if (init_f == NULL)
    {
        fprintf(stderr, "No file to be read\n");
        return 2;
    }
    //Define buffer to store memory in
    BYTE buffer[512];
    //Define file number
    int f_nr = 0;
    //Define file to be written
    FILE *new_f;
    //Define name of file to be written
    char f_name[8] = {0};
    //Repeat reading from file
    while (fread(buffer, sizeof(buffer), 1, init_f) == 1)
    {
        //Checking for beggining of JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //If this is the first JPEG found
            if (f_nr == 0)
            {
                //Name the JPEG
                sprintf(f_name, "%03i.jpg", f_nr);
                //Increase file number for next JPEG
                f_nr ++;
                //Open new file for writing
                new_f = fopen(f_name, "w");
                //Writing new file
                fwrite(buffer, sizeof(buffer), 1, new_f);

            }
            else
            {
                //If this is not the first JPEG found
                if (f_nr > 0)
                {
                    //Close opened file
                    fclose(new_f);
                    //Name the new JPEG
                    sprintf(f_name, "%03i.jpg", f_nr);
                    //Increase file number for next JPEG
                    f_nr ++;
                    //Open new file for writing
                    new_f = fopen(f_name, "w");
                    //Writing new file
                    fwrite(buffer, sizeof(buffer), 1, new_f);
                }
            }
        }
        else{
            if (f_nr > 0)
            {
               //Continue to write new file
                fwrite(buffer, sizeof(buffer), 1, new_f);
            }
        }
    }
    //Closing all open files
    fclose(new_f);
    fclose(init_f);
    return 0;

}
