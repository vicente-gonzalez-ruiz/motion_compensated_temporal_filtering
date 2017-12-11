#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Dyadic spatial resolution transcoding.

# Extracts a codestream from a bigger one, discarding a number of
# spatial resolutions.

# Reducing the number of spatial resolutions is trivial, using the
# facility provided by the image transcoder, because to performe a
# transcoding, all the images can be trancoded discarding the highest
# spatial resolution levels, and the motion information must be
# interpreted in this case as if over-pixel ME/MC had been
# performed. For example, if one spatial resolution level is
# discarded, the degree of over-pixel ME/MC should be incremented by
# one.

# Examples:
#
#   mctf transcode_resolution --SRLs=2
