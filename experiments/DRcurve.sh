#!/bin/bash

video=~/Videos/mobile_352x288x30x420x300.yuv
GOPs=9
TRLs=6
y_dim=288
x_dim=352
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

while getopts "v:p:x:y:f:q:g:?" opt; do
    case ${opt} in
        v)
            video="${OPTARG}"
            ;;
        x)
            x_dim="${OPTARG}"
            ;;
        y)
            y_dim="${OPTARG}"
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
ln -s ~/Videos/container_352x288x30x420x300.yuv low_0
mctf compress --GOPs=$GOPs --TRLs=$TRLs
mctf info --GOPs=$GOPs --TRLs=$TRLs
lines=`wc -l ~/.bashrc | cut -f 1 -d " "`
mkdir transcode_quality
rm container_DRcurve.dat

for i in `seq 1 $lines`;
do
    echo Running for layers=$i
    mctf transcode_quality --GOPs=$GOPs --TRLs=TRLs --layers=$i
    cp motion*.j2c transcode_quality
    cp *type* transcode_quality
    cd transcode_quality
    rate=`mctf info --GOPs=$GOPs --TRLs=$TRLs --pictures_per_second=$FPS | grep "Total average:" | cut -d " " -f 5`
    echo -n $rate >> container_DRcurve.dat
    mctf expand --GOPs=9 --TRLs=6
    RMSE=`snr --file_A=../low_0 --file_B=low_0 2> /dev/null | grep RMSE | cut -f 3`
    cd ..
    echo $RMSE >> container_DRcurve.dat
done
set +x
