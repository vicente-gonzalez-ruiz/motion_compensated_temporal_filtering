#!/bin/bash

VIDEO=~/Videos/mobile_352x288x30x420x300.yuv
GOPs=9
TRLs=6
Y_DIM=288
X_DIM=352
FPS=30

usage() {
    echo $0
    echo "  [-v video file name ($VIDEO)]"
    echo "  [-g GOPs ($GOPs)]"
    echo "  [-x X dimension ($X_DIM)]"
    echo "  [-y Y dimension ($Y_DIM)]"
    echo "  [-f frames/second ($FPS)]"
    echo "  [-t ($TRLs)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "v:p:x:y:f:q:g:?" opt; do
    case ${opt} in
	v)
	    VIDEO="${OPTARG}"
	    ;;
	x)
	    X_DIM="${OPTARG}"
	    ;;
	y)
	    Y_DIM="${OPTARG}"
	    ;;
	f)
	    FPS="${OPTARG}"
	    ;;
	t)
	    TRLs="${TRLs}"
	    ;;
	g)
	    GOPs="${GOPs}"
	    ;;
	?)
            usage
            exit 0
            ;;
        \?)
            echo "Invalid option: -${OPTARG}" >&2
            usage
            exit 1
            ;;
        :)
            echo "Option -${OPTARG} requires an argument." >&2
	    usage
            exit 1
            ;;
    esac
done

set -x

ln -s $VIDEO low_0
mctf compress --GOPs=$GOPs --TRLs=$TRLs
mctf info --GOPs=$GOPs --TRLs=$TRLs
mkdir tmp
cd tmp
cp ../*.j2c .
cp ../slopes.tx .
cp ../*type* .
mctf expand --GOPs=$GOPs --TRLs=$TRLs
mctf show
mkdir transcode_quality
mctf transcode_quality --GOPs=$GOPs --TRLs=$TRLs
cp ../motion*.j2c .
cp ../*type* .
mctf info --GOPs=$GOPs --TRLs=$TRLs
mctf expand --GOPs=$GOPs --TRLs=$TRLs
mctf show
