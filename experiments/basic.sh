#!/bin/bash

video=~/Videos/mobile_352x288x30x420x300.avi
GOPs=9
TRLs=6
y_dim=288
x_dim=352
FPS=30
keep_layers=8

usage() {
    echo $0
    echo "  [-v video file name ($video)]"
    echo "  [-g GOPs ($GOPs)]"
    echo "  [-x X dimension ($x_dim)]"
    echo "  [-y Y dimension ($y_dim)]"
    echo "  [-f frames/second ($FPS)]"
    echo "  [-t TRLs ($TRLs)]"
    echo "  [-k keep layers ($keep_layers)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "v:p:x:y:f:t:g:k:?" opt; do
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
	k)
	    keep_layers="${OPTARG}"
	    echo keep_layers=$keep_layers
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

rm -rf low_0
mkdir low_0
ffmpeg -i $video -c:v rawvideo -pix_fmt yuv420p low_0/%4d.Y
x_dim_2=`echo $x_dim/2 | bc`
y_dim_2=`echo $y_dim/2 | bc`
for i in low_0/*.Y
do
    rawtopgm $x_dim $y_dim < $i > $i.pgm
done
for i in low_0/*.U
do
    rawtopgm $x_dim_2 $y_dim_2 < $i > $i.pgm
done
for i in low_0/*.V
do
    rawtopgm $x_dim_2 $y_dim_2 < $i > $i.pgm
done

#ffmpeg -i $video low_0/%4d.pgm
exit
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
mctf transcode_quality --GOPs=$GOPs --TRLs=$TRLs --keep_layers=$keep_layers
cd transcode_quality
#cp ../motion*.j2c .
cp ../*type* .
mctf info --GOPs=$GOPs --TRLs=$TRLs
mctf expand --GOPs=$GOPs --TRLs=$TRLs
mctf show
