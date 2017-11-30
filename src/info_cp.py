#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from info import info

class info_cp(info):

    def find_next_EOC_texture(self, file):
        """Does nothing"""
        return 0

    def find_next_EOC_motion(self, file):
        """Does nothing"""
        return 0

    def open_codestream(self, codestream_filename):
        """Open a RAW (YUV) code-stream"""
        return open(codestream_filename + ".cp", 'rb')

x=info_cp() # ?
