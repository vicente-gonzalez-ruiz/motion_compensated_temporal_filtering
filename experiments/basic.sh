#!/bin/bash

video=~/Videos/mobile_352x288x30x420x300.yuv
GOPs=9
TRLs=6
y_dim=288
x_dim=352
FPS=30

usage() {
    echo $0
    echo "  [-v video file name ($video)]"
    echo "  [-g GOPs ($GOPs)]"
    echo "  [-x X dimension ($x_dim)]"
    echo "  [-y Y dimension ($y_dim)]"
    echo "  [-f frames/second ($FPS)]"
    echo "  [-t TRLs ($TRLs)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "v:p:x:y:f:t:g:?" opt; do
    case ${opt} in
	v)
	    video="${OPTARG}"
	    echo video=$video
	    ;;
	x)
	    x_dim="${OPTARG}"
	    echo x_dim=$x_dim
	    ;;
	y)
	    y_dim="${OPTARG}"
	    echo y_dim=$y_dim
	    ;;
	f)
	    FPS="${OPTARG}"
	    echo FPS=$FPS
	    ;;
	t)
	    TRLs="${OPTARG}"
	    echo TRLs=$TRLs
	    ;;
	g)
	    GOPs="${OPTARG}"
	    echo GOPs=$GOPs
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

rm low_0
ln -s $video low_0
mctf compress --GOPs=$GOPs --TRLs=$TRLs
mctf info --GOPs=$GOPs --TRLs=$TRLs
mkdir tmp
cd tmp
cp ../*.j2c .
cp ../*type* .
cp ../*.txt .
mctf expand --GOPs=$GOPs --TRLs=$TRLs
mctf show
mkdir transcode_quality
mctf transcode_quality --GOPs=$GOPs --TRLs=$TRLs
cd transcode_quality
#cp ../motion*.j2c .
cp ../*type* .
mctf info --GOPs=$GOPs --TRLs=$TRLs
mctf expand --GOPs=$GOPs --TRLs=$TRLs
mctf show
