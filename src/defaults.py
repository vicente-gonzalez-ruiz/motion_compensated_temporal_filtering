#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

# Default parameters for all Python scripts.

class Defaults():

    # Forces to use only B frames.
    always_B = 0

    # Number of overlaped pixels between the blocks in the motion
    # compensation process.
    block_overlaping = 0

    # Size of the blocks in the motion estimation process.
    block_size = 32

    # Size of the border of the blocks in the motion estimation process.
    border_size = 0

    # Number of Group Of Pictures to process (apart from GOP 0).
    GOPs = 1

    # Minimal block size allowed in the motion estimation process.
    min_block_size = 32

    # Of the ME process.
    max_search_range = 128

    # Logarithm controls the quality level and the bit-rate of the
    # code-stream of motions.
    motion_layers = 1

    # Width of the pictures.
    pixels_in_x = 352

    # Height of the pictures.
    pixels_in_y = 288

    # Distance in the quantization step, between quality layers in the
    # same subband. (Kakadu uses 256 by default).
    quantization_step = 0

    # Controls the quality level and the bit-rate of the code-stream
    # of motions.
    motion_quantization = 45000
    
    # Controls the quality level and the bit-rate of the code-stream
    # of textures.
    texture_quantization = 45000

    # Size of the search areas in the motion estimation process.
    search_range = 4

    # Refers to Full-HD resolution. Is used as a boundary between the
    # use of a block size of 16 or 32 by default.
    #resolution_FHD       = 1920 * 1080

    # Number of Spatial Resolution Levels.
    SRLs = 5

    # Subpixel motion estimation order.
    subpixel_accuracy = 0

    # Number of layers. Logarithm controls the quality level and the
    # bit-rate of the code-stream.
    texture_layers = 8

    # Number of Temporal Resolution Levels.
    TRLs = 4

    # Weight of the update step.
    update_factor = 0 # 1.0/4

    # Calculates the quantifications from the gains or not. Default:
    # gains. Anything else (example "nogains"), do not use the gains.
    using_gains = "gains"
