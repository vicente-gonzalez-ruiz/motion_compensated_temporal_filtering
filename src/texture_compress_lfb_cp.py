#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
from subprocess import check_call
from subprocess import CalledProcessError
from MCTF_parser import MCTF_parser

file = ""

parser = MCTF_parser(description="Does nothing with the LFB texture data.")
parser.add_argument("--file", help="file that contains the LFB data. Default = {})".format(file))

args = parser.parse_known_args()[0]
if args.file:
    file = args.file

try:
    check_call("trace cp " + file + " " + file + ".cp", shell=True)
except CalledProcessError:
    sys.exit(-1)
