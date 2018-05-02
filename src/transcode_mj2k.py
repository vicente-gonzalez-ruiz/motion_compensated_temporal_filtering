#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-
#
## @file transcode_mj2k.py
#  Extracts a number of quality layers. Extracts a number of layers of
#  an encoded video quality, with more than one quality layer. The
#  result is the same, that have fewer layers specified quality (via
#  their corresponding "slopes") in the "compress" command.
#
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.
#
#  @example transcode_mj2k.py
#
#  - Typical script.\n
#  mctf compress --slopes="44000,43500,43000" \n
#  mctf extract --layers=2 \n
#  mctf expand

## @package transcode_mj2k
#  Extracts a number of quality layers. Extracts a number of layers of
#  an encoded video quality, with more than one quality layer. The
#  result is the same, that have fewer layers specified quality (via
#  their corresponding "slopes") in the "compress" command.


#  DEBUG:
#  The option to extract images, transcode the matter, and back
#  together seems not to work. Try parsing option .mj2 stream directly,
#  letting you copy the output data that belong to quality layers,
#  which should not be removed. In addition, this option is more
#  efficient and can be applied to pipes.
#  Note: SOC = 0xFF4F
#        EOC = 0xFFD9


import sys
import getopt
import os
import array
import display
import string

## Refers to high frequency subbands.
HIGH = "high"
## Refers to low frequency subbands.
LOW = "low"
## Number of extracted quality layers.
layers = 1
## Number of images to process.
pictures = 33
## Width of the pictures.
pixels_in_x = 352
## Height of the pictures.
pixels_in_y = 288
## Number of iterations of the temporal transform + 1.
temporal_levels = 6

## Documentation of usage.
#  - -[-l]ayers = number of extracted quality layers.
#  - -[-p]ictures = number of images to process.
#  - -[-]pixels_in_[x] = size of the X dimension of the pictures.
#  - -[-]pixels_in_[y] = size of the Y dimension of the pictures.
#  - -[-t]emporal_levels = number of iterations of the temporal transform + 1.
def usage():
    sys.stderr.write("+--------------+\n")
    sys.stderr.write("| MCTF extract |\n")
    sys.stderr.write("+--------------+\n")
    sys.stderr.write("\n")
    sys.stderr.write("  Description:\n")
    sys.stderr.write("\n")
    sys.stderr.write("   Extracts a number of quality layers.\n")
    sys.stderr.write("\n")
    sys.stderr.write("  Parameters:\n")
    sys.stderr.write("\n")
    sys.stderr.write("   -[-l]ayers=number of extracted quality layers (\"%d\")\n" % layers)
    sys.stderr.write("   -[-p]ictures=number of images to process (%d)\n" % pictures)
    sys.stderr.write("   -[-]pixels_in_[x]=size of the X dimension of the pictures (%d)\n" %  pixels_in_x)
    sys.stderr.write("   -[-]pixels_in_[y]=size of the Y dimension of the pictures (%d)\n" %  pixels_in_y)
    sys.stderr.write("   -[-t]emporal_levels=number of iterations of the temporal transform + 1 (%d)\n" % temporal_levels)
    sys.stderr.write("\n")

## Define the variable for options.
opts = ""

ifdef({{DEBUG}},
display.info(str(sys.argv[0:]) + '\n')
)

try:
    opts, extraparams = getopt.getopt(sys.argv[1:],"l:p:x:y:t:h",
                                      ["layers=",
                                       "pictures=",
                                       "pixels_in_x=",
                                       "pixels_in_y=",
                                       "temporal_levels=",
                                       "help"
                                       ])
except getopt.GetoptError, exc:
    sys.stderr.write(sys.argv[0] + ": " + exc.msg + "\n")
    sys.exit(2)

## Define the variable for params.
params = ""
    
for o, a in opts:
    if o in ("-l", "--layers"):
        layers = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": layers=" + str(layers) + '\n')
        )
    if o in ("-p", "--pictures"):
        pictures = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": pictures=" + str(pictures) + '\n')
        )
    if o in ("-x", "--pixels_in_x"):
        pixels_in_x = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": pixels_in_x=" + str(pixels_in_x) + '\n')
        )
    if o in ("-y", "--pixels_in_y"):
        pixels_in_y = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": pixels_in_y=" + str(pixels_in_y) + '\n')
        )
    if o in ("-t", "--temporal_levels"):
        temporal_levels = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": temporal_levels=" + str(temporal_levels) + '\n')
        )
    if o in ("-h", "--help"):
	usage()
	sys.exit()


## Current temporal iteration.
subband = 1

## Extracts a number of quality layers.
command = "mkdir extract"
ifdef({{DEBUG}},
display.info(sys.argv[0] + ": " + command + "\n")
)
os.system(command)



# Handles the HIGH frequency subbands.
#-------------------------------------
while subband < temporal_levels:

    ifdef({{DEBUG}},
    display.info(sys.argv[0] + ": processing high-pass subband " + str(subband) + " of " + str(temporal_levels) + "\n")
    )

    ## Name of the input file.
    entrada = HIGH + "_" + str(subband) + ".mj2"

    ## Name of the output file.
    salida = "extract/" + entrada

    # Copy the file header '.mj2'.
    command = "dd if=" + entrada + " of=" + salida + " skip=0 ibs=1 count=20"
    ifdef({{DEBUG}},
    display.info(sys.argv[0] + ": " + command + "\n")
    )
    os.system(command)

    ## Open the input file, now to find the EOC (0xFFD9) of each
    ## image.
    f = open(entrada, "r")

    ## Skip the 20 bytes of header '.mj2'.
    startImage = 20
    f.seek(startImage, 0)

    ## Bytes extraction begins:
    byte = f.read(1)
    while byte != '':
        if byte == '\xff':
            byte = f.read(1)
            if byte == '\xd9':
                ## Jumps to the end of the image.
                endImage = f.tell()

                # Extract the image.
                command = "dd if=" + entrada + " of=image_Aux.j2c skip=" + str(startImage) + " ibs=1 count=" + str(endImage - startImage)
                ifdef({{DEBUG}},
                display.info(sys.argv[0] + ": " + command + "\n")
                )
                os.system(command)

                # Extracts the first layer (s) of quality.
                command = "kdu_transcode -i image_Aux.j2c -o image_Out.j2c Clayers=" + str(layers)
                ifdef({{DEBUG}},
                display.info(sys.argv[0] + ": " + command + "\n")
                )
                os.system(command)

                # Add the generated image.
                command = "cat image_Out.j2c >> " + salida
                ifdef({{DEBUG}},
                display.info(sys.argv[0] + ": " + command + "\n")
                )
                os.system(command)
            
                # Concatenate '0x0000179A' at the end of "exit".
                command = "dd if=" + entrada + " of=/tmp/extract.tmp skip=" + str(endImage) + " bs=1 count=4" 
                ifdef({{DEBUG}},
                display.info(sys.argv[0] + ": " + command + "\n")
                )
                os.system(command)
                command = "cat /tmp/extract.tmp >> " + salida
                ifdef({{DEBUG}},
                display.info(sys.argv[0] + ": " + command + "\n")
                )
                os.system(command)

                # Skip the last 4 bytes of padding.
                startImage = endImage + 4

        byte = f.read(1)

    f.close

    subband += 1

subband -= 1


# Handles the LOW frequency subbands.
#-------------------------------------
ifdef({{DEBUG}},
display.info(sys.argv[0] + ": processing low-pass subband " + str(subband) + " of " + str(temporal_levels) + "\n")
)

# Name of the input file.
entrada = LOW + "_" + str(subband) + ".mj2"

# Name of the output file.
salida = "extract/" + entrada

# Copy the file header '.mj2'.
command = "dd if=" + entrada + " of=" + salida + " skip=0 ibs=1 count=20"
ifdef({{DEBUG}},
display.info(sys.argv[0] + ": " + command + "\n")
)
os.system(command)

# Open the input file, now to find the EOC (0xFFD9) of each
# image.
f = open(entrada, "r")

# Skip the 20 bytes of header '.mj2'.
startImage = 20
f.seek(startImage, 0)

# Bytes extraction begins:
byte = f.read(1)
while byte != '':
    if byte == '\xff':
        byte = f.read(1)
        if byte == '\xd9':
            endImage = f.tell()

            # Extract the image.
            command = "dd if=" + entrada + " of=image_Aux.j2c skip=" + str(startImage) + " ibs=1 count=" + str(endImage - startImage)
            ifdef({{DEBUG}},
            display.info(sys.argv[0] + ": " + command + "\n")
            )
            os.system(command)

            # Extracts the first layer (s) of quality.
            command = "kdu_transcode -i image_Aux.j2c -o image_Out.j2c Clayers=" + str(layers)
            ifdef({{DEBUG}},
            display.info(sys.argv[0] + ": " + command + "\n")
            )
            os.system(command)

            # Add the generated image.
            command = "cat image_Out.j2c >> " + salida
            ifdef({{DEBUG}},
            display.info(sys.argv[0] + ": " + command + "\n")
            )
            os.system(command)

            # Concatenate '0x0000179A' at the end of "exit".
            command = "dd if=" + entrada + " of=/tmp/extract.tmp skip=" + str(endImage) + " bs=1 count=4" 
            ifdef({{DEBUG}},
            display.info(sys.argv[0] + ": " + command + "\n")
            )
            os.system(command)
            command = "cat /tmp/extract.tmp >> " + salida
            ifdef({{DEBUG}},
            display.info(sys.argv[0] + ": " + command + "\n")
            )
            os.system(command)

            # Skip the last 4 bytes of padding.
            startImage = endImage + 4

    byte = f.read(1)

f.close
