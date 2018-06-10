#!/bin/bash

low="L_0/"
even="E_1/"
odd="O_1/"
pictures=33
pixels_in_x=352
pixels_in_y=288

usage() {
    echo $0
    echo "Forward Lazzy wavelet transform over the time domain"
    echo "  [-e even pictures ($even)]"
    echo "  [-o odd pictures ($odd)]"
    echo "  [-l low pictures ($low)]"
    echo "  [-p pictures ($pictures)]"
    echo "  [-x pixels_in_x ($pixels_in_x)]"
    echo "  [-y pixels_in_y ($pixels_in_y)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "e:o:l:p:x:y:?" opt; do
    case ${opt} in
	e)
	    even="${OPTARG}"
	    echo even=$even
	    ;;
	o)
	    odd="${OPTARG}"
	    echo odd=$odd
	    ;;
	l)
	    low="${OPTARG}"
	    echo low=$low
	    ;;
	p)
	    pictures="${OPTARG}"
	    echo pictures=$pictures
	    ;;
	x)
	    pixels_in_x="${OPTARG}"
	    echo $0: pixels_in_x=$pixels_in_x
	    ;;
	y)
	    pixels_in_y="${OPTARG}"
	    echo $0: pixels_in_y=$pixels_in_y
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

mkdir $low

ln -s ../${even}/"0000_0.pgm" $low
ln -s ../${even}/"0000_1.pgm" $low
ln -s ../${even}/"0000_2.pgm" $low

picture=0
pictures_2=`echo $pictures/2-1 | bc`
while [ $picture -le $pictures_2 ]
do
    _odd=`echo $picture*2+1 | bc`
    ln -s ../$odd/$(printf "%04d_0.pgm" $picture) $low/$(printf "%04d_0.pgm" $_odd)
    ln -s ../$odd/$(printf "%04d_1.pgm" $picture) $low/$(printf "%04d_1.pgm" $_odd)
    ln -s ../$odd/$(printf "%04d_2.pgm" $picture) $low/$(printf "%04d_2.pgm" $_odd)

    _even=`echo $picture*2+2 | bc`
    ((picture++))
    ln -s ../$even/$(printf "%04d_0.pgm" $picture) $low/$(printf "%04d_0.pgm" $_even)
    ln -s ../$even/$(printf "%04d_1.pgm" $picture) $low/$(printf "%04d_1.pgm" $_even)
    ln -s ../$even/$(printf "%04d_2.pgm" $picture) $low/$(printf "%04d_2.pgm" $_even)

done
