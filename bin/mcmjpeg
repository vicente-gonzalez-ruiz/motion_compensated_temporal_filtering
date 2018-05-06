#! /bin/bash

## \file mcmjpeg.sh
#  \brief Assigns the codec MCMJPEG to environment variables. They
#   will be needed by other script.
#  
#  \author Vicente Gonzalez-Ruiz.
#  \date Last modification: 2015, January 7.

## \brief MCTF texture codec.
export MCTF_TEXTURE_CODEC="mjpeg"

## \brief MCTF motion codec.
export MCTF_MOTION_CODEC="j2k"

## \brief Slopes sample.
export SLOPES="30"


if [[ "$1" != "info" ]] ; then
    mctf $@
else
    mctf $1_jpg $2 $3
fi
