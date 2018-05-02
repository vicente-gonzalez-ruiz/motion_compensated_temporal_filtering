#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

## @file display.py
#  Bridge of communication between the programming language and display system.
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package display
#  Bridge of communication between the programming language and display system.

import sys

## Makes a system call in order to display information about the execution.
#  @param string Information about the execution.
def info(string):
    sys.stderr.write(string)
    sys.stderr.flush()

## Makes a system call in order to display error information about the execution.
#  @param string Error information about the execution.
def error(string):
    sys.stderr.write("[0;31m")
    sys.stderr.write("Fatal error: ")
    sys.stderr.write(string)
    sys.stderr.write("Aborting!")
    sys.stderr.write("[1;0m")
    sys.stderr.flush()
    sys.exit()

## Makes a system call in order to display warning information on implementation.
#  @param string Warning information on implementation.
def warning(string):
    sys.stderr.write("[0;34m")
    sys.stderr.write("Warning: ")
    sys.stderr.write(string)
    sys.stderr.write("[1;0m")
    sys.stderr.flush()
