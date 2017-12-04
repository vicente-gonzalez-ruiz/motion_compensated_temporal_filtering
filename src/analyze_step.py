#!/usr/bin/python
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

## Y dimension of a picture.
pixels_in_y         = 288
## Number of Groups Of Pictures of the scene.
GOPs                = 1
## Number of Temporal resolution Levels.
TRLs                = 4
## Initializes the variable, temporal subband a '1'.
temporal_subband    = 1
## Requires that all generated images are of type 'B'.
always_B            = 0
## Number of pixels of overlap between blocks.
block_overlaping    = 0
## Size of a block.
block_size          = 32
## Border size or margin of a block.
border_size         = 0
## Total number of video images.
pictures            = 9
## Search range for motion vectors.
search_range        = 4
## Sub-pixel accuracy in motion estimate.
subpixel_accuracy   = 0
## Level update. For example, a value equal to 1/4 means that the high-frequency subband is 4 times less important than the low-frequency subband.
update_factor       = 0 # 1.0/4

parser = arguments_parser(description="Performs a temporal analysis step.")
parser.pictures()
parser.search_range()
parser.subpixel_accuracy()
parser.update_factor()

args = parser.parse_known_args()[0]

parser.pixels_in_x()
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)

parser.pixels_in_y()
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)

parser.GOPs()
if args.GOPs:
    GOPs = int(args.GOPs)

parser.TRLs()
if args.TRLs:
    TRLs = int(args.TRLs)

parser.temporal_subband()
if args.temporal_subband:
    temporal_subband = int(args.temporal_subband)

parser.always_B()
if args.always_B:
    always_B = int(args.always_B)

parser.block_overlaping(block_overlaping)
if args.block_overlaping:
    block_overlaping = int(args.block_overlaping)

resolution_FHD = 1920 * 1080
parser.block_size()
parser.border_size()
if pixels_in_x * pixels_in_y < resolution_FHD:
    block_size = 32
else:
    block_size = 64
if args.block_size:
    block_size = int(args.block_size)

parser.border_size()
if args.border_size:
    border_size = int(args.border_size)

if args.pictures:
    pictures = int(args.pictures)
if args.search_range:
    search_range = int(args.search_range)
if args.subpixel_accuracy:
    subpixel_accuracy = int(args.subpixel_accuracy)
if args.update_factor:
    update_factor = float(args.update_factor)

try :
    # Lazzy transform.
    check_call("mctf split"
               + " --even_fn="     + "even_" + str(temporal_subband)
               + " --low_fn="      + "low_"  + str(temporal_subband-1)
               + " --odd_fn="      + "odd_"  + str(temporal_subband)
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
               + " --even_fn="           + "even_"    + str(temporal_subband)
               + " --imotion_fn="        + "imotion_" + str(temporal_subband)
               + " --motion_fn="         + "motion_"  + str(temporal_subband)
               + " --odd_fn="            + "odd_"     + str(temporal_subband)
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
    f_motion = open ("motion_" + str(temporal_subband), 'r')
    # f_image  = open ("motion_" + str(temporal_subband) + "_importance_image", 'w')
    f_sub    = open ("motion_" + str(temporal_subband) + "_importance_sub"  , 'w')

    # A null motion vector.
    VM_cero         = '\x00\x00\x00\x00\x00\x00\x00\x00'
    # Images in the subband.
    nImages_sub     = pow (2, TRLs - temporal_subband - 1) * GOPs
    # Images in the subband for each GOP.
    nImages_gop_sub = pow (2, TRLs - temporal_subband - 1)

    # Blocks in the image.
    nBloques_image  = (pixels_in_x * pixels_in_y) / (block_size * block_size)
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
        motion_importance = 1 - (nCeros / nBloques_sub)
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
               + " --even_fn="           + "even_"            + str(temporal_subband)
               + " --frame_types_fn="    + "frame_types_"     + str(temporal_subband)
               + " --high_fn="           + "high_"            + str(temporal_subband)
               + " --motion_in_fn="      + "motion_"          + str(temporal_subband)
               + " --motion_out_fn="     + "motion_filtered_" + str(temporal_subband)
               + " --odd_fn="            + "odd_"             + str(temporal_subband)
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
               + " --even_fn="           + "even_"            + str(temporal_subband)
               + " --frame_types_fn="    + "frame_types_"     + str(temporal_subband)
               + " --high_fn="           + "high_"            + str(temporal_subband)
               + " --low_fn="            + "low_"             + str(temporal_subband)
               + " --motion_fn="         + "motion_filtered_" + str(temporal_subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               + " --update_factor="     + str(update_factor)
               , shell=True)
except CalledProcessError :
    sys.exit(-1)
