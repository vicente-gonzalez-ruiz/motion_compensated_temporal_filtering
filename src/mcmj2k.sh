#! /bin/bash


## \file mcmj2k.sh
#  \brief Assigns the codec MCMJ2K to environment variables. They
#   will be needed by other script.
#  
#  \author Vicente Gonzalez-Ruiz.
#  \date Last modification: 2015, January 7.

## \brief MCTF texture codec.
export MCTF_TEXTURE_CODEC="mj2k"

## \brief MCTF motion codec.
export MCTF_MOTION_CODEC="j2k"

## \brief Slopes sample.
export SLOPES="44500,44250,44000,43700,43400"

## \brief Transcode algorithm.
export TRANSCODE_QUALITY="transcode_quality_FSO"
#export TRANSCODE_QUALITY="transcode_quality_PLT"


if [[ "$1" != "info" ]] ; then
    mctf $@
else
    mctf $1_mj2k $2 $3 $4
fi
