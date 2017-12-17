#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

#  Iteration of the temporal transform.

import sys
import os
import traceback
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser

parser = arguments_parser(description="Performs a temporal analysis step.")
parser.add_argument("--pictures",
                    help="number of pictures to analyze",
                    default=33)
parser.search_range()
parser.subpixel_accuracy()
parser.update_factor()
parser.pixels_in_x()
parser.pixels_in_y()
parser.GOPs()
parser.TRLs()
parser.temporal_subband()
parser.always_B()
parser.block_overlaping()
parser.block_size()
parser.border_size()

args = parser.parse_known_args()[0]
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
GOPs = int(args.GOPs)
TRLs = int(args.TRLs)
subband = int(args.temporal_subband)
always_B = int(args.always_B)
block_overlaping = int(args.block_overlaping)
block_size = int(args.block_size)
border_size = int(args.border_size)
pictures = int(args.pictures)
search_range = int(args.search_range)
subpixel_accuracy = int(args.subpixel_accuracy)
update_factor = float(args.update_factor)

try :
    # Lazzy transform.
    check_call("mctf split"
               + " --even_fn="     + "even_" + str(subband)
               + " --low_fn="      + "low_"  + str(subband-1)
               + " --odd_fn="      + "odd_"  + str(subband)
               + " --pictures="    + str(pictures)
               + " --pixels_in_x=" + str(pixels_in_x)
               + " --pixels_in_y=" + str(pixels_in_y)
               , shell=True)
except CalledProcessError :
    sys.exit(-1)

try :
    # Motion estimation.
    check_call("mctf motion_estimate"
               + " --block_size="        + str(block_size)
               + " --border_size="       + str(border_size)
               + " --even_fn="           + "even_"    + str(subband)
               + " --imotion_fn="        + "imotion_" + str(subband)
               + " --motion_fn="         + "motion_"  + str(subband)
               + " --odd_fn="            + "odd_"     + str(subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --search_range="      + str(search_range)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               , shell=True)
except Exception:
    print("Exception {} when calling mctf motion_estimate".format(traceback.format_exc()))
    sys.exit(-1)

## Additional code for research work. Expressed as a percentage of the amount of motion vectors that do not indicate a linear motion between frames.
def amount_motion () :

    ## Number of components of a motion field.
    COMPONENTS      = 4
    ## Number of bytes for each component.
    BYTES_COMPONENT = 2
    ## Number of bytes of a motion field.
    BYTES_VM        = COMPONENTS * BYTES_COMPONENT
    
    # Motion vectors file.
    f_motion = open ("motion_" + str(subband), 'r')
    # f_image  = open ("motion_" + str(subband) + "_importance_image", 'w')
    f_sub    = open ("motion_" + str(subband) + "_importance_sub"  , 'w')

    # A null motion vector.
    VM_cero         = '\x00\x00\x00\x00\x00\x00\x00\x00'
    # Images in the subband.
    nImages_sub     = pow (2, TRLs - subband - 1) * GOPs
    # Images in the subband for each GOP.
    nImages_gop_sub = pow (2, TRLs - subband - 1)

    # Blocks in the image.
    nBloques_image  = (pixels_in_x * pixels_in_y) // (block_size * block_size)
    # Blocks in the subband.
    nBloques_sub    = nBloques_image * nImages_gop_sub

    # Number of bytes in an image, which relate to motion vectors.
    bytes_image     = nBloques_image * BYTES_VM
    # Number of bytes in an subband, which relate to motion vectors.
    bytes_gop       = bytes_image * nImages_gop_sub

    # Percentage of zeros for each subband.
    for iGOP in range (0, GOPs) : # for each GOP
        # Initializes percentage of zeros for each subband.
        nCeros = 0.0
        for iBlock in range (0, nBloques_sub) : # Iterates over each block in a subband.
            if f_motion.read(BYTES_VM) in VM_cero :
                nCeros += 1.0
        motion_importance = 1 - (nCeros // nBloques_sub)
        f_sub.write (str(motion_importance) + "\n")

    f_sub.close ()
    f_motion.close ()

# Call amount_motion
# amount_motion()

try :
    # Motion Compensation.
    check_call("mctf decorrelate"
               + " --block_overlaping="  + str(block_overlaping)
               + " --block_size="        + str(block_size)
               + " --even_fn="           + "even_"            + str(subband)
               + " --frame_types_fn="    + "frame_types_"     + str(subband)
               + " --high_fn="           + "high_"            + str(subband)
               + " --motion_in_fn="      + "motion_"          + str(subband)
               + " --motion_out_fn="     + "motion_filtered_" + str(subband)
               + " --odd_fn="            + "odd_"             + str(subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --search_range="      + str(search_range)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               + " --always_B="          + str(always_B)
               , shell=True)
except CalledProcessError :
    sys.exit(-1)

try :
    # Eliminate the temporal aliasing (smoothing).
    check_call("mctf update"
               + " --block_size="        + str(block_size)
               + " --even_fn="           + "even_"            + str(subband)
               + " --frame_types_fn="    + "frame_types_"     + str(subband)
               + " --high_fn="           + "high_"            + str(subband)
               + " --low_fn="            + "low_"             + str(subband)
               + " --motion_fn="         + "motion_filtered_" + str(subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               + " --update_factor="     + str(update_factor)
               , shell=True)
except CalledProcessError :
    sys.exit(-1)
