#!/bin/bash

low="low_0"
even="even_1"
odd="odd_1"
images=33

usage() {
    echo $0
    echo "Direct Lazzy wavelet transform over the time domain"
    echo "  [-e even images ($even)]"
    echo "  [-o odd images ($odd)]"
    echo "  [-l low images ($low)]"
    echo "  [-i images ($images)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "e:o:l:i:?" opt; do
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
	i)
	    images="${OPTARG}"
	    echo images=$images
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

mkdir $even
mkdir $odd

ln -s ../${low}/"0000_0.pgm" $even
ln -s ../${low}/"0000_1.pgm" $even
ln -s ../${low}/"0000_2.pgm" $even

image=0
images_2=`echo $images/2 | bc`
while [ $image -le $images_2 ]
do
    _odd=`echo $image*2+1 | bc`
    ln -s ../$low/$(printf "%04d_0.pgm" $_odd) $odd/$(printf "%04d_0.pgm" $image)
    ln -s ../$low/$(printf "%04d_1.pgm" $_odd) $odd/$(printf "%04d_1.pgm" $image)
    ln -s ../$low/$(printf "%04d_2.pgm" $_odd) $odd/$(printf "%04d_2.pgm" $image)

    _even=`echo $image*2+2 | bc`
    ((image++))
    ln -s ../$low/$(printf "%04d_0.pgm" $_even) $even/$(printf "%04d_0.pgm" $image)
    ln -s ../$low/$(printf "%04d_1.pgm" $_even) $even/$(printf "%04d_1.pgm" $image)
    ln -s ../$low/$(printf "%04d_2.pgm" $_even) $even/$(printf "%04d_2.pgm" $image)

done
