#! /bin/bash


## \file MCLTW.sh
#  \brief Assigns the codec MCLTW to environment variables. They
#   will be needed by other script.
#  
#  \author Vicente Gonzalez-Ruiz.
#  \date Last modification: 2015, January 7.

## \brief MCTF texture codec.
export MCTF_TEXTURE_CODEC="ltw"

## \brief MCTF motion codec.
export MCTF_MOTION_CODEC="j2k"

## \brief Slopes sample.
export SLOPES="4.0"


if [[ "$1" != "info" ]] ; then
    mctf $@
else
    mctf $1_ltw $2 $3
fi
