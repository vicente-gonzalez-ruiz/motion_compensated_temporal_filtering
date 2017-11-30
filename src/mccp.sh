#! /bin/bash

## \file mccp.sh
#  \brief Assigns the codec MCCP to environment variables. They
#   will be needed by other script.
#  
#  \author Vicente Gonzalez-Ruiz.
#  \date Last modification: 2015, January 7.

## \brief MCTF texture codec.
export MCTF_TEXTURE_CODEC="cp"

## \brief MCTF motion codec.
export MCTF_MOTION_CODEC="j2k"

if [[ "$1" != "info" ]] ; then
    mctf $@
else
    mctf $1_cp $2 $3 $4
fi
