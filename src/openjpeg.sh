#! /bin/bash

## \file openjpeg.sh
#  \brief Assigns the codec OPENJPEG to environment variables. They will
#   be needed by other script.
#  
#  \author Vicente Gonzalez-Ruiz.
#  \date Last modification: 2015, January 7.

## \brief MCTF texture codec.
export MCTF_TEXTURE_CODEC="image_to_j2k"

## \brief MCTF motion codec.
export MCTF_MOTION_CODEC="image_to_j2k"

if [[ "$1" != "info" ]] ; then
    mctf $@
else
    mctf $1_j2k $2 $3 $4
fi
