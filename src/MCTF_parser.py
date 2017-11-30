#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

## @file MCTF_parser.py
#  Command-line interfaces.
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package MCTF_parser
#  Command-line interfaces.


import argparse

## The argparse module makes it easy to write user-friendly command-line interfaces.
class MCTF_parser(argparse.ArgumentParser):

#    def __init__(self, parser):
#        super(MCTF_parser, self).__init__(parser)
#    def __init__(self, *p):
#        super(MCTF_parser, self).__init__(*p)

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param always_B Forces to use only B frames.
    def always_B(self, always_B):
        self.add_argument("--always_B", help="forces to use only B frames. (Default = {})".format(always_B))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param block_overlaping Number of overlaped pixels between the blocks in the motion compensation process.
    def block_overlaping(self, block_overlaping):
        self.add_argument("--block_overlaping", help="number of overlaped pixels between the blocks in the motion compensation process. (Default = {})".format(block_overlaping))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param block_size Size of the blocks in the motion estimation process.
    def block_size(self, block_size):
        self.add_argument("--block_size", help="size of the blocks in the motion estimation process. (Default = {})".format(block_size))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param block_size_min Minimal block size allowed in the motion estimation process.
    def block_size_min(self, block_size_min):
        self.add_argument("--block_size_min", help="minimal block size allowed in the motion estimation process. (Default = {})".format(block_size_min))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param border_size Size of the border of the blocks in the motion estimation process.
    def border_size(self, border_size):
        self.add_argument("--border_size", help="size of the border of the blocks in the motion estimation process. (Default = {})".format(border_size))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param GOPs Number of Group Of Pictures to process.
    def GOPs(self, GOPs):
        self.add_argument("--GOPs", help="number of Group Of Pictures to process. (Default = {})".format(GOPs))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param pictures Number of images to process.
    def pictures(self, pictures):
        self.add_argument("--pictures", help="number of images to process. (Default = {})".format(pictures))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param pixels_in_x Width of the pictures.
    def pixels_in_x(self, pixels_in_x):
        self.add_argument("--pixels_in_x", help="width of the pictures. (Default = {})".format(pixels_in_x))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param pixels_in_y Height of the pictures.
    def pixels_in_y(self, pixels_in_y):
        self.add_argument("--pixels_in_y", help="height of the pictures. (Default = {})".format(pixels_in_y))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param clayers_motion Logarithm controls the quality level and the bit-rate of the code-stream of motions.
    def clayers_motion(self, clayers_motion):
        self.add_argument("--clayers_motion", help="logarithm controls the quality level and the bit-rate of the code-stream of motions. (Default = {})".format(clayers_motion))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param clayers Logarithm controls the quality level and the bit-rate of the code-stream.
    def clayers(self, clayers):
        self.add_argument("--clayers", help="logarithm controls the quality level and the bit-rate of the code-stream. (Default = {})".format(clayers))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param nLayers Number of layers. Logarithm controls the quality level and the bit-rate of the code-stream.
    def nLayers(self, nLayers):
        self.add_argument("--nLayers", help="Number of layers. Logarithm controls the quality level and the bit-rate of the code-stream. (Default = {})".format(nLayers))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param BRC Bit-Rate control.
    def BRC(self, BRC):
        self.add_argument("--BRC", help="Bit-Rate control. (Default = {})".format(BRC))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param rates Read only the initial portion of the code-stream, corresponding to an overall bit-rate of \"rate\" bits/sample.
    def rates(self, rates):
        self.add_argument("--rates", help="Read only the initial portion of the code-stream, corresponding to an overall bit-rate of \"rate\" bits/sample. (Default = {})".format(rates))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param quantization_step Distance in the quantization step, between quality layers in the same subband. (kakadu used by default 256).
    def quantization_step(self, quantization_step):
        self.add_argument("--quantization_step", help="Distance in the quantization step, between quality layers in the same subband. kakadu used by default 256. (Default = {})".format(quantization_step))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param quantization_motion Controls the quality level and the bit-rate of the code-stream of motions.
    def quantization_motion(self, quantization_motion):
        self.add_argument("--quantization_motion", help="controls the quality level and the bit-rate of the code-stream of motions. (Default = {})".format(quantization_motion))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param quantization_texture Controls the quality level and the bit-rate of the code-stream of textures.
    def quantization_texture(self, quantization_texture):
        self.add_argument("--quantization_texture", help="controls the quality level and the bit-rate of the code-stream of textures. (Default = {})".format(quantization_texture))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param quantization Controls the quality level and the bit-rate of the code-stream.
    def quantization(self, quantization):
        self.add_argument("--quantization", help="controls the quality level and the bit-rate of the code-stream. (Default = {})".format(quantization))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param using_gains Controls the slopes for quality layers.
    def using_gains(self, using_gains):
        self.add_argument("--using_gains", help="controls the slopes for quality layers. (Default = {})".format(using_gains))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param search_range Size of the search areas in the motion estimation process.
    def search_range(self, search_range):
        self.add_argument("--search_range", help="size of the search areas in the motion estimation process. (Default = {})".format(search_range))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param subpixel_accurary Subpixel motion estimation order.
    def subpixel_accuracy(self, subpixel_accurary):
        self.add_argument("--subpixel_accuracy", help="subpixel motion estimation order. (Default = {})".format(subpixel_accurary))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param TRLs Number of Temporal Resolution Levels.
    def TRLs(self, TRLs):
        self.add_argument("--TRLs", help="number of Temporal Resolution Levels. (Default = {})".format(TRLs))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param SRLs Number of Spatial Resolution Levels.
    def SRLs(self, SRLs):
        self.add_argument("--SRLs", help="number of Spatial Resolution Levels. (Default = {})".format(SRLs))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param subband Number of subband.
    def subband(self, subband):
        self.add_argument("--subband", help="number of subband. (Default = {})".format(subband))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param update_factor Weight of the update step.
    def update_factor(self, update_factor):
        self.add_argument("--update_factor", help="weight of the update step. (Default = {})".format(update_factor))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param FPS Frames per second.
    def FPS(self, FPS):
        self.add_argument("--FPS", help="frames per second. (Default = {})".format(FPS))

    ## Command-line interface for a parameter.
    # @param self Refers to object.
    # @param distortions Number of Group Of Pictures to process.
    def distortions(self, distortions):
        self.add_argument("--distortions", help="Path file which in each line there a distortion (PSNR) per frame. (Default = {})".format(distortions))

#   def temporal_levels(self, temporal_levels):
#       self.add_argument("--temporal_levels", help="number of temporal levels. (Default = {})".format(temporal_levels))
