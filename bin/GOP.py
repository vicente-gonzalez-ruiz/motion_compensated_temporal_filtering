#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

## @file GOP.py
#  Class defines a group of pictures.
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package GOP
#  Class defines a group of pictures.

## Group of Pictures.
class GOP:

    ## Calculates the GOP size based on the number of temporal levels.
    # @param self Refers to object.
    # @param temporal_levels Number of temporal levels.
    # @returns The GOP size.
    def get_size(self, temporal_levels):
        return 2**(temporal_levels - 1)
