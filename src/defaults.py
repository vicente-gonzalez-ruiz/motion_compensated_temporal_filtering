#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Default values for common Python script parameters.

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

    # Number of Group Of Pictures to process.
    GOPs = 2 # GOP_0 always have only one picture.

    # Minimal block size allowed in the motion estimation process.
    min_block_size = 32

    # Width of the pictures.
    pixels_in_x = 352

    # Height of the pictures.
    pixels_in_y = 288

    # Controls the quality level and the bit-rate of the code-stream
    # of motions.
    motion_layers = 1
    motion_quantization = 0 # 0 -> No quantization
    motion_quantization_step = 0
    motion_slopes = "0"
    
    # Size of the search areas in the motion estimation process.
    search_range = 4

    # Number of Spatial Resolution Levels.
    SRLs = 5

    # Subpixel motion estimation order.
    subpixel_accuracy = 0

    # Texture quantization.
    #layers = 8
    quantization_min = 42000 # Max quality
    #quantization_min = 45000
    quantization_max = 50000 # Min quality
    quantization_step = 1024 # If smaller than 256, possible empty layers
    #texture_slopes = "43000, 43256, 43512, 43768, 44024, 44280, 44536, 44792"
    #quantization_max = 50000
    #quantization_min = 42000
    #quality = 0.5 # 1.0 = max, 0.0 = min
    
    # Number of Temporal Resolution Levels.
    TRLs = 6 # GOP_size = 32

    # Weight of the update step.
    update_factor = 0 # 1.0/4 # 0 -> No updating.
