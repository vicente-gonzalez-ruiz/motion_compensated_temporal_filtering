#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

## @file call.py
#  Bridge of communication between the programming language and operating system.
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package call
#  Bridge of communication between the programming language and operating system.

import sys
import os

## Makes a system call and check that no errors occurred.
#  @param string System call instruction.
def call(string):
    x = os.system(string)
    if x!=0:
        sys.exit()

