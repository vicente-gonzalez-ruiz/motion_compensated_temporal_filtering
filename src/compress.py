#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

## @file compress.py
#  Compression of a sequence of images (motion vectors and textures).
#  The compression consists of three major steps:\n
#  - Temporal analysis of image sequence. Temporal decorrelation.
#  - Compress the fields of motion. A layer quality is used without loss.
#  - Compressed textures. Quality layers are used, with loss.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.
#
#  @example compress.py
#
#  - Show default parameters.\n
#  mcj2k compress --help
#
#  - Compress using the default parameters.\n
#  mcj2k compress
#
#  - Using a GOP_size=8.\n
#  mcj2k compress --TRLs=3
#
#  - Controlling quantization.
#  mcj2k compress --quantization=45000
#
#  - Example of use.\n 
#  compress --update_factor=0 --nLayers=16
#  --quantization_texture=42000 --GOPs=10 --TRLs=5 --SRLs=5
#  --block_size=32 --block_size_min=32 --search_range=4
#  --pixels_in_x=352 --pixels_in_y=288

## @package compress
#  Compression of a sequence of images (motion vectors and textures).
#  The compression consists of three major steps:\n
#  - Temporal analysis of image sequence. Temporal decorrelation.
#  - Compress the fields of motion. A layer quality is used without loss.
#  - Compressed textures. Quality layers are used, with loss.


import sys
import getopt
import os
import array
import display
import string
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from MCTF_parser import MCTF_parser

## Refers to Full-HD resolution. Is used as a boundary between the use
#  of a block size of 16 or 32 by default.
resolution_FHD       = 1920 * 1080
## Width of the pictures.
pixels_in_x          = 352
## Height of the pictures.
pixels_in_y          = 288
## Forces to use only B frames.
always_B             = 0
## Number of overlaped pixels between the blocks in the motion
#  compensation process.
block_overlaping     = 0
## Size of the blocks in the motion estimation process.
block_size           = 32
## Minimal block size allowed in the motion estimation process.
block_size_min       = 32
## Size of the border of the blocks in the motion estimation process.
border_size          = 0
## Number of Group Of Pictures to process.
GOPs                 = 1
## Logarithm controls the quality level and the bit-rate of the
#  code-stream of motions.
clayers_motion       = 0
## Distance in the quantization step, between quality layers in the
#  same subband. (kakadu used by default 256).
quantization_step    = 0
## Controls the quality level and the bit-rate of the code-stream of
#  motions.
quantization_motion  = 45000
## Controls the quality level and the bit-rate of the code-stream of
#  textures.
quantization_texture = 45000
## Size of the search areas in the motion estimation process.
search_range         = 4
## Subpixel motion estimation order.
subpixel_accuracy    = 0
## Number of Temporal Resolution Levels.
TRLs                 = 4
## Number of Spatial Resolution Levels.
SRLs                 = 5
## Number of layers. Logarithm controls the quality level and the
#  bit-rate of the code-stream.
nLayers              = 5
## Weight of the update step.
update_factor        = 1.0/4
## Calculates the quantifications from the gains or not. Default: gains. Anything else (example "nogains"), do not use the gains.
using_gains          = "gains"

## The parser module provides an interface to Python's internal parser
#  and byte-code compiler.
parser = MCTF_parser(description="Encodes a sequence of pictures.")
parser.pixels_in_x(pixels_in_x)
parser.pixels_in_y(pixels_in_y)
parser.always_B(always_B)
parser.block_overlaping(block_overlaping)
parser.block_size(block_size)
parser.block_size_min(block_size_min)
parser.border_size(border_size)
parser.GOPs(GOPs)
parser.clayers_motion(clayers_motion)
parser.quantization_step(quantization_step)
parser.quantization_motion(quantization_motion)
parser.quantization_texture(quantization_texture)
parser.search_range(search_range)
parser.subpixel_accuracy(subpixel_accuracy)
parser.TRLs(TRLs)
parser.SRLs(SRLs)
parser.nLayers(nLayers)
parser.update_factor(update_factor)
parser.using_gains(using_gains)

## A script may only parse a few of the command-line arguments,
#  passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)
if args.always_B:
    always_B = int(args.always_B)
if args.block_overlaping:
    block_overlaping = int(args.block_overlaping)

# Default block_size as pixels_in_xy
if pixels_in_x * pixels_in_y < resolution_FHD:
    block_size = block_size_min = 32
else:
    block_size = block_size_min = 64

if args.block_size:
    block_size = int(args.block_size)
if args.block_size_min:
    block_size_min = int(args.block_size_min)
    
if args.border_size:
    border_size = int(args.border_size)
if args.GOPs:
    GOPs = int(args.GOPs)
if args.clayers_motion:
    clayers_motion = str(args.clayers_motion)
if args.quantization_step:
    quantization_step = args.quantization_step
if args.quantization_motion:
    quantization_motion = str(args.quantization_motion) # Jse: int -> str
if args.quantization_texture:
    quantization_texture = str(args.quantization_texture)
if args.search_range:
    search_range = int(args.search_range)
if args.subpixel_accuracy:
    subpixel_accuracy = int(args.subpixel_accuracy)
if args.TRLs:
    TRLs = int(args.TRLs)
if args.SRLs:
    SRLs = int(args.SRLs)
if args.nLayers:
    nLayers = int(args.nLayers)
if args.update_factor:
    update_factor = float(args.update_factor)
if args.using_gains:
    using_gains = str(args.using_gains)



if TRLs > 1:
    try:
        # Temporal analysis of image sequence. Temporal decorrelation.
        #-------------------------------------------------------------
        check_call("mctf analyze"
                   + " --always_B="          + str(always_B)
                   + " --block_overlaping="  + str(block_overlaping)
                   + " --block_size="        + str(block_size)
                   + " --block_size_min="    + str(block_size_min)
                   + " --border_size="       + str(border_size)
                   + " --GOPs="              + str(GOPs)
                   + " --pixels_in_x="       + str(pixels_in_x)
                   + " --pixels_in_y="       + str(pixels_in_y)
                   + " --search_range="      + str(search_range)
                   + " --subpixel_accuracy=" + str(subpixel_accuracy)
                   + " --TRLs="              + str(TRLs)
                   + " --update_factor="     + str(update_factor)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        # Compress the fields of motion. A layer quality is used without loss.
        #---------------------------------------------------------------------
        check_call("mctf motion_compress"
                   + " --block_size="     + str(block_size)
                   + " --block_size_min=" + str(block_size_min)
                   + " --GOPs="           + str(GOPs)
                   + " --pixels_in_x="    + str(pixels_in_x)
                   + " --pixels_in_y="    + str(pixels_in_y)
                   + " --quantization=\"" + str(quantization_motion) + "\""
                   + " --clayers=\""      + str(clayers_motion) + "\""
                   + " --SRLs="           + str(SRLs)
                   + " --TRLs="           + str(TRLs)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

try:
    # Compressed textures. Quality layers are used, with loss.
    #---------------------------------------------------------
    check_call("mctf texture_compress"
               + " --GOPs="                + str(GOPs)
               + " --pixels_in_x="         + str(pixels_in_x)
               + " --pixels_in_y="         + str(pixels_in_y)
               + " --quantization=\""      + str(quantization_texture) + "\""
               + " --quantization_step="   + str(quantization_step)
               + " --SRLs="                + str(SRLs)
               + " --TRLs="                + str(TRLs)
               + " --nLayers="             + str(nLayers)
               + " --using_gains="         + str(using_gains)
               , shell=True)
except CalledProcessError:
    sys.exit(-1)


