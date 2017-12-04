#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

# Default parameters for all Python scripts.

class Defaults():

    resolution_FHD       = 1920 * 1080 ## Refers to Full-HD
                                       #  resolution. Is used as a
                                       #  boundary between the use of
                                       #  a block size of 16 or 32 by
                                       #  default.
    pixels_in_x          = 352         ## Width of the pictures.
    pixels_in_y          = 288         ## Height of the pictures.
    always_B             = 0           ## Forces to use only B frames.
    block_overlaping     = 0           ## Number of overlaped pixels
                                       #  between the blocks in the
                                       #  motion compensation process.
    block_size           = 32          ## Size of the blocks in the
                                       #  motion estimation process.
    block_size_min       = 32          ## Minimal block size allowed
                                       #  in the motion estimation
                                       #  process.
    border_size          = 0           ## Size of the border of the
                                       #  blocks in the motion
                                       #  estimation process.
    GOPs                 = 1           ## Number of Group Of Pictures
                                       #  to process (apart from GOP
                                       #  0).
    quantization_step    = 0           ## Distance in the quantization
                                       #  step, between quality layers
                                       #  in the same subband. (Kakadu
                                       #  uses 256 by default).
    quantization_motion  = 45000       ## Controls the quality level
                                       #  and the bit-rate of the
                                       #  code-stream of motions.
    quantization_texture = 45000       ## Controls the quality level
                                       #  and the bit-rate of the
                                       #  code-stream of textures.
    search_range         = 4           ## Size of the search areas in
                                       #  the motion estimation
                                       #  process.
    subpixel_accuracy    = 0           ## Subpixel motion estimation
                                       #  order.
    TRLs                 = 4           ## Number of Temporal
                                       #  Resolution Levels.
    SRLs                 = 5           ## Number of Spatial Resolution
                                       #  Levels.
    texture_layers       = 8           ## Number of layers. Logarithm
                                       #  controls the quality level
                                       #  and the bit-rate of the
                                       #  code-stream.
    motion_layers        = 1           ## Logarithm controls the
                                       #  quality level and the
                                       #  bit-rate of the code-stream
                                       #  of motions.
    update_factor        = 0 # 1.0/4   ## Weight of the update step.
    using_gains = "gains"              ## Calculates the
                                       #  quantifications from the
                                       #  gains or not. Default:
                                       #  gains. Anything else
                                       #  (example "nogains"), do not
                                       #  use the gains.
