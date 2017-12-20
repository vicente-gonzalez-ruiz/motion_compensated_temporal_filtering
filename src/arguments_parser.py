#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import argparse
from defaults import Defaults

class arguments_parser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(arguments_parser, self).__init__(*args, **kwargs, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def always_B(self):
        self.add_argument("--always_B",
                          help="Use only B frames.",
                          default=Defaults.always_B)

    def block_overlaping(self):
        self.add_argument("--block_overlaping",
                          help="Number of overlaped pixels between the "
                          "blocks in the motion compensation process.",
                          default=Defaults.block_overlaping)

    def block_size(self):
        self.add_argument("--block_size",
                          help="Size of the blocks in the motion estimation",
                          default=Defaults.block_size)

    def border_size(self):
        self.add_argument("--border_size",
                          help="Size of the border of the blocks "
                          "in the motion estimation process.",
                          default=Defaults.border_size)

    # Unused?
    def distortions(self):
        self.add_argument("--distortions",
                          help="Path file which in each line there a "
                          "distortion (PSNR) per frame.",
                          default=Defaults.distortions)
    # Unused?
    def FPS(self):
        self.add_argument("--FPS",
                          help="frames per second.",
                          default=Defaults.FPS)

    def GOPs(self):
        self.add_argument("--GOPs",
                          help="Group Of Pictures to process.",
                          default=Defaults.GOPs)

    def max_search_range(self):
        self.add_argument("--max_search_range",
                          help="Maximum search range allowed during ME.",
                          default=Defaults.max_search_range)
        
    def min_block_size(self):
        self.add_argument("--min_block_size",
                          help="Minimal block size allowed during ME.",
                          default=Defaults.min_block_size)

    def motion_layers(self):
        self.add_argument("--motion_layers",
                          help="Number of quality layers for motion subbands. ",
                          default=Defaults.motion_layers)

    def motion_quantization(self):
        self.add_argument("--motion_quantization",
                          help="Controls the quality level and the bit-rate "
                          "of the code-stream of motion data.",
                          default=Defaults.motion_quantization)

    # No aquí?
    #def pictures(self):
    #    self.add_argument("--pictures",
    #                      help="number of images to process.",
    #                      default=Defaults.pictures)

    def pixels_in_x(self):
        self.add_argument("--pixels_in_x",
                          help="Width of the pictures.",
                          default=Defaults.pixels_in_x)

    def pixels_in_y(self):
        self.add_argument("--pixels_in_y",
                          help="Height of the pictures.",
                          default=Defaults.pixels_in_y)

    def quantization_step(self):
        self.add_argument("--quantization_step",
                          help="Distance in the quantization step, "
                          "between quality layers in the same subband. "
                          "Kakadu uses by default 256.",
                          default=Defaults.quantization_step)

    # Unused?
    #def rates(self):
    #    self.add_argument("--rates",
    #                      help="Read only the initial portion of the "
    #                      "code-stream, corresponding to an overall bit-rate "
    #                      "of \"rate\" bits/sample.",
                          default=Defaults.rates)

    def search_range(self):
        self.add_argument("--search_range",
                          help="Size (in pixels) of the search areas "
                          "in the motion estimation process.",
                          default=Defaults.search_range)

    def SRLs(self):
        self.add_argument("--SRLs",
                          help="Spatial Resolution Levels.",
                          default=Defaults.SRLs)

    def subpixel_accuracy(self):
        self.add_argument("--subpixel_accuracy",
                          help="Subpixel motion estimation precission",
                          default=Defaults.subpixel_accuracy)

    def texture_layers(self):
        self.add_argument("--texture_layers",
                          help="Number of quality layers for "
                          "texture subbands. ",
                          default=Defaults.texture_layers)

    def texture_quantization(self):
        self.add_argument("--texture_quantization",
                          help="Controls the quality level and the bit-rate "
                          "of the code-stream of texture data.",
                          default=Defaults.texture_quantization)
                          
    def TRLs(self):
        self.add_argument("--TRLs",
                          help="Temporal Resolution Levels.",
                          default=Defaults.TRLs)

    # Not here?
    #def temporal_subband(self):
    #    self.add_argument("--temporal_subband",
    #                      help="number of the temporal subband.",
    #                      default=0)

    def update_factor(self):
        self.add_argument("--update_factor",
                          help="Weight of the update step of MCTF.",
                          default=Defaults.update_factor)

    #def using_gains(self):
    #    self.add_argument("--using_gains",
    #                      help="Weights the temporal subband slopes.",
    #                      default=Defaults.using_gains) # Yes or Not
