#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file expand.py
#  Decodes a sequence of pictures.
#  Decoding consists of two major steps:\n
#  - Decompression textures and movement data.
#  - Synthesizes the video.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.
#  @example expand.py
#
#  - Show default parameters.\n
#  mcj2k expand --help
#
#  - Expands using the default parameters.\n
#  mcj2k expand
#
#  - Example of use.\n
#  expand --update_factor=0 --GOPs=1 --TRLs=5 --SRLs=5 --block_size=32
#  --block_size_min=32 --search_range=4 --pixels_in_x=352
#  --pixels_in_y=288 --subpixel_accuracy=0

## @package expand
#  Decodes a sequence of pictures.
#  Decoding consists of two major steps:\n
#  - Decompression textures and movement data.
#  - Synthesizes the video.



import sys
import display
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from MCTF_parser import MCTF_parser

## Refers to Full-HD resolution. Is used as a boundary between the use
## of a block size of 16 or 32 by default.
resolution_FHD    = 1920 * 1080
## Number of Temporal Resolution Levels.
TRLs              = 4
## Width of the pictures.
pixels_in_x       = "352,352,352,352"
## Height of the pictures.
pixels_in_y       = "288,288,288,288"
## Size of the blocks in the motion estimation process.
block_size        = "32,32,32"
## Minimal block size allowed in the motion estimation process.
block_size_min    = 32
## Number of Group Of Pictures to process.
GOPs              = 1
## Number of Spatial Resolution Levels.
SRLs              = 5
## Optional and developing parameter indicates whether to extract the
#  codestream to a given bit-rate. The bit-rate control is performed
#  in transcode.py, a detailed manner, and therefore its use is
#  recommended for this purpose.
rates             = "0.0,0.0,0.0,0.0,0.0"
## Subpixel motion estimation order.
subpixel_accuracy = "0,0,0,0,0"
## Size of the search areas in the motion estimation process.
search_range      = 4
## Size of the border of the blocks in the motion estimation process.
border_size       = 0
## Number of overlaped pixels between the blocks in the motion
## compensation process.
block_overlaping  = 0
## Weight of the update step.
update_factor     = 1.0/4

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = MCTF_parser(description="Decodes a sequence of pictures.")
parser.TRLs(TRLs)
parser.pixels_in_x(pixels_in_x)
parser.pixels_in_y(pixels_in_y)
parser.block_size(block_size)
parser.block_size_min(block_size_min)
parser.GOPs(GOPs)
parser.SRLs(SRLs)
parser.rates(rates)
parser.subpixel_accuracy(subpixel_accuracy)
parser.search_range(search_range)
parser.border_size(border_size)
parser.block_overlaping(block_overlaping)
parser.update_factor(update_factor)

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.TRLs:
    TRLs = int(args.TRLs)
if args.pixels_in_x:
    pixels_in_x = str(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = str(args.pixels_in_y)

# Default block_size as pixels_in_xy
if int(pixels_in_x.split(',')[0]) * int(pixels_in_y.split(',')[0]) < resolution_FHD:
    block_size     = ','.join(['32'] * (TRLs-1))
    block_size_min = 32
else:
    block_size     = ','.join(['64'] * (TRLs-1))
    block_size_min = 64

if args.block_size:
    block_size = str(args.block_size)
if args.block_size_min:
    block_size_min = int(args.block_size_min)
if args.GOPs:
    GOPs = int(args.GOPs)
if args.SRLs:
    SRLs = int(args.SRLs)
if args.rates:
    rates = str(args.rates)
if args.subpixel_accuracy:
    subpixel_accuracy = str(args.subpixel_accuracy)
if args.search_range:
    search_range = int(args.search_range)
if args.border_size:
    border_size = int(args.border_size)
if args.block_overlaping:
    block_overlaping = int(args.block_overlaping)
if args.update_factor:
    update_factor = float(args.update_factor)




## Sets parameters resized from the number of TRL.
#  @param block_size Size of the blocks in the motion estimation process.
#  @param rates Optional and developing parameter indicates whether to extract the codestream to a given bit-rate. The bit-rate control is performed in transcode.py, a detailed manner, and therefore its use is recommended for this purpose.
#  @param pixels_in_x Width of the pictures.
#  @param pixels_in_y Height of the pictures.
#  @param subpixel_accuracy Subpixel motion estimation order.
#  @param TRLs Number of Temporal Resolution Levels.
#  @return _block_size (list)
#  @return _rates (list)
#  @return _pixels_in_x (list)
#  @return _pixels_in_y (list)
#  @return _subpixel_accuracy (list)
#  @return block_size (string)
#  @return rates (string)
#  @return pixels_in_x (string)
#  @return pixels_in_y (string)
#  @return subpixel_accuracy (string)
def set_parameters (block_size, rates, pixels_in_x, pixels_in_y, subpixel_accuracy, TRLs):

    # string -> list
    #---------------
    _block_size        = block_size.split(',')
    _rates             = rates.split(',')
    _pixels_in_x       = pixels_in_x.split(',')
    _pixels_in_y       = pixels_in_y.split(',')
    _subpixel_accuracy = subpixel_accuracy.split(',')


    # Resizes the parameters
    #-----------------------

    # block_size
    for i in range ( len(_block_size), TRLs-1 ) :
        if int(_block_size[len(_block_size)-1]) > block_size_min :
            _block_size.append(int(_block_size[len(_block_size)-1]) /2)
        else :
            _block_size.append(int(_block_size[len(_block_size)-1])   )

    # rates
    for i in range ( len(_rates), TRLs ) :
        _rates.append(_rates[len(_rates)-1])

    # pixels_in_x
    for i in range ( len(_pixels_in_x), TRLs ) :
        _pixels_in_x.append(_pixels_in_x[len(_pixels_in_x)-1])

    # pixels_in_y
    for i in range ( len(_pixels_in_y), TRLs ) :
        _pixels_in_y.append(_pixels_in_y[len(_pixels_in_y)-1])

    # subpixel_accuracy
    for i in range ( len(_subpixel_accuracy), TRLs ) :
        _subpixel_accuracy.append(_subpixel_accuracy[len(_subpixel_accuracy)-1])

    # list -> string
    #---------------
    block_size        = str(','.join(map(str, _block_size)))
    rates             = str(','.join(map(str, _rates)))
    pixels_in_x       = str(','.join(map(str, _pixels_in_x)))
    pixels_in_y       = str(','.join(map(str, _pixels_in_y)))
    subpixel_accuracy = str(','.join(map(str, _subpixel_accuracy)))


    # Displays the parameters resized from the number of TLRs, 
    # in order to verify that it has been carried out without errors.
    #----------------------------------------------------------------
    # check_call("echo \"\n--block_size=" + str(block_size)
    #           + "\n--pixels_in_x=" + str(pixels_in_x)
    #           + "\n--pixels_in_y=" + str(pixels_in_y)
    #           + "\n--subpixel_accuracy=" + str(subpixel_accuracy) + "\""
    #           , shell=True)
    # raw_input("")

    return _block_size, _rates, _pixels_in_x, _pixels_in_y, _subpixel_accuracy, block_size, rates, pixels_in_x, pixels_in_y, subpixel_accuracy


_block_size, _rates, _pixels_in_x, _pixels_in_y, _subpixel_accuracy, block_size, rates, pixels_in_x, pixels_in_y, subpixel_accuracy = set_parameters(block_size, rates, pixels_in_x, pixels_in_y, subpixel_accuracy, TRLs)





# Time
# /usr/bin/time -f "# Real-User-System\n%e\t%U\t%S" -a -o "info_time" date
# /usr/bin/time -f "%e\t%U\t%S" -a -o "info_time_" date



# Decompression textures.
#------------------------
try:
    check_call("/usr/bin/time -f \"%e\t%U\t%S\t(TRLs:" + str(TRLs) + ")\" -a -o \"../info_time_texture_expand\" mctf texture_expand"
               + " --GOPs="        + str(GOPs)
               + " --rates="       + str(rates)
               + " --pixels_in_x=" + str(pixels_in_x)
               + " --pixels_in_y=" + str(pixels_in_y)
               + " --SRLs="        + str(SRLs)
               + " --TRLs="        + str(TRLs)
               , shell=True)
except CalledProcessError:
    sys.exit(-1)


# Decompression movement data.
#-----------------------------
if TRLs > 1 :
    try:
        check_call("/usr/bin/time -f \"%e\t%U\t%S\t(TRLs:" + str(TRLs) + ")\" -a -o \"../info_time_motion_expand\" mctf motion_expand"
                   + " --block_size="  + str(block_size)
                   + " --GOPs="        + str(GOPs)
                   + " --pixels_in_x=" + str(pixels_in_x)
                   + " --pixels_in_y=" + str(pixels_in_y)
                   + " --TRLs="        + str(TRLs)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    # Synthesizes the video.
    #-----------------------
    try:
        check_call("/usr/bin/time -f \"%e\t%U\t%S\t(TRLs:" + str(TRLs) + ")\" -a -o \"../info_time_synthesize\" mctf synthesize"
                   + " --GOPs="              + str(GOPs)
                   + " --TRLs="              + str(TRLs)
                   + " --block_size="        + str(block_size)
                   + " --pixels_in_x="       + str(pixels_in_x)
                   + " --pixels_in_y="       + str(pixels_in_y)
                   + " --subpixel_accuracy=" + str(subpixel_accuracy)
                   + " --search_range="      + str(search_range)
                   + " --block_overlaping="  + str(block_overlaping)
                   + " --update_factor="     + str(update_factor)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)
