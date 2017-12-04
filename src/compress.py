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
import arguments_parser

parser = arguments_parser(description="Encodes a sequence of pictures.")
args = parser.parse_known_args()[0]

parser.pixels_in_x()
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)

parser.pixels_in_y()
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)

parser.always_B()
if args.always_B:
    always_B = int(args.always_B)

parser.block_overlaping()
if args.block_overlaping:
    block_overlaping = int(args.block_overlaping)

# Default block_size as pixels_in_xy
resolution_FHD = 1920 * 1080
parser.block_size()
parser.block_size_min()
if pixels_in_x * pixels_in_y < resolution_FHD:
    block_size = block_size_min = 32
else:
    block_size = block_size_min = 64
if args.block_size:
    block_size = int(args.block_size)
if args.block_size_min:
    block_size_min = int(args.block_size_min)
    
parser.border_size()
if args.border_size:
    border_size = int(args.border_size)

parser.GOPs()
if args.GOPs:
    GOPs = int(args.GOPs)

parser.clayers_motion()
if args.clayers_motion:
    clayers_motion = str(args.clayers_motion)

parser.quantization_step()
if args.quantization_step:
    quantization_step = args.quantization_step

parser.quantization_motion()
if args.quantization_motion:
    quantization_motion = str(args.quantization_motion)

parser.quantization_texture()
if args.quantization_texture:
    quantization_texture = str(args.quantization_texture)

parser.search_range()
if args.search_range:
    search_range = int(args.search_range)

parser.subpixel_accuracy()
if args.subpixel_accuracy:
    subpixel_accuracy = int(args.subpixel_accuracy)

parser.TRLs()
if args.TRLs:
    TRLs = int(args.TRLs)

parser.SRLs()
if args.SRLs:
    SRLs = int(args.SRLs)

parser.nLayers()
if args.nLayers:
    nLayers = int(args.nLayers)

parser.update_factor()
if args.update_factor:
    update_factor = float(args.update_factor)

parser.using_gains()
if args.using_gains:
    using_gains = str(args.using_gains)

if TRLs > 1:
    try:
        # Temporal analysis of image sequence. Temporal decorrelation.
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
