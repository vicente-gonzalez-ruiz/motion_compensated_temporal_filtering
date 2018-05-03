#!/bin/bash

set -x
ln -s ~/Videos/container_352x288x30x420x300.yuv low_0
mctf compress --GOPs=9 --TRLs=6
mctf info --GOPs=9 --TRLs=6
lines=`wc -l ~/.bashrc | cut -f 1 -d " "`
mkdir transcode_quality
rm container_DRcurve.dat

for i in `seq 1 $lines`;
do
    echo Running for layers=$i
    mctf transcode_quality --GOPs=9 --TRLs=6 --layers=$i
    cp motion*.j2c transcode_quality
    cp *type* transcode_quality
    cd transcode_quality
    bps=`mctf info --GOPs=9 --TRLs=6 | tail -n 1 | cut -d " " -f 5`
    echo -n $bps >> container_DRcurve.dat
    mctf expand --GOPs=9 --TRLs=6
    psnr=`mctf psnr --file_A=../low_0 --file_B=low_0`
    echo $psnr >> container_DRcurve.dat
done
set +x
