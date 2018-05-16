#!/bin/bash

low="low_0/"
even="even_1/"
odd="odd_1/"
pictures=33

usage() {
    echo $0
    echo "Forward Lazzy wavelet transform over the time domain"
    echo "  [-e even pictures ($even)]"
    echo "  [-o odd pictures ($odd)]"
    echo "  [-l low pictures ($low)]"
    echo "  [-p pictures ($pictures)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "e:o:l:p:?" opt; do
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

ln -s ../${even}"0000_Y" $low
ln -s ../${even}"0000_U" $low
ln -s ../${even}"0000_V" $low

picture=0
pictures_2=`echo $pictures/2 | bc`
while [ $picture -le $pictures_2 ]
do
    _odd=`echo $picture*2+1 | bc`
    ln -s ../$odd$(printf "%04d.Y.pgm" $picture) $low/$(printf "%04d.Y.pgm" $_odd)
    ln -s ../$odd$(printf "%04d.U.pgm" $picture) $low/$(printf "%04d.U.pgm" $_odd)
    ln -s ../$odd$(printf "%04d.V.pgm" $picture) $low/$(printf "%04d.V.pgm" $_odd)

    _even=`echo $picture*2+2 | bc`
    ln -s ../$even$(printf "%04d.Y.pgm" $picture) $low/$(printf "%04d.Y.pgm" $_even)
    ln -s ../$even$(printf "%04d.U.pgm" $picture) $low/$(printf "%04d.U.pgm" $_even)
    ln -s ../$even$(printf "%04d.V.pgm" $picture) $low/$(printf "%04d.V.pgm" $_even)

    ((picture++))
done
