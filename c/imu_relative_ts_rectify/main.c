#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "imu_rectify.h"

#define APP_NAME "imu_rectify"
#define APP_VERSION "0.2"

static void Usage(void)
{
    printf("Usage:\n");
    printf("  %s [options] filename[.ext]\n", APP_NAME);
    printf(
            "    input_filename      SBP binary or SBP JSON input file. Note, only binary supported at present.\n\n");
    printf("Options:\n");
    printf("  -o output_filename    Override default output filename.");
    printf("\n");
    return;

} // Usage()

int main(int argc, char* argv[]) {
    char filename[1024] = "";
    char output_filename[1024] = "";
    char ini_filename[1024] = "";
    char cfg_filename[1024] = "posefilter.cfg";
    printf("%s v%s.\n", APP_NAME, APP_VERSION);

    if (argc < 2)
            {
        printf("  unwrap / rectifity relative to PPS imu or wheeltick timestamps in Swift Binary Protocol log file(s).\n");
        printf("ERROR: not enough parameters.\n\n");
        Usage();
        exit(1);
    }

    // Process options ---------------------------------------------------------
    int i = 1;
    while (i < argc)
    {
        // Output File --------------------------------------------------
        if (0 == strcmp("-o", argv[i]))
        {
            i++;
            if (argc < i + 1)
                    {
                printf("\nERROR: not enough parameters for -o option.\n\n");
                Usage();
                exit(1);
            }
            else {
                strncpy(output_filename, argv[i], sizeof(output_filename) - 1);
            }
        }
        else
        {
            strncpy(filename, argv[i], sizeof(filename) - 1);
        }
        i++;
    } // while()

    if (0 == strlen(filename))
            {
        printf("\nERROR: file name is empty.\n\n");
        exit(1);
    }
    if (0 == strlen(output_filename))
            {
        strncpy(output_filename, filename, sizeof(output_filename) - 1);
        strncat(output_filename, ".imu_rectify.sbp", sizeof(output_filename) - 1);
        printf("using default output filename: %s\n", output_filename);
    }
   return imu_rectify(filename, output_filename);
}
