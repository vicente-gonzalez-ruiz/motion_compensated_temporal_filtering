#!/bin/bash

low_fn  = "low_0/"
even_fn = "even_1/"
odd_fn  = "odd_1/"
images  = 33

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

ln -s ${low}"0000.Y.pgm" $even
ln -s ${low}"0000.U.pgm" $even
ln -s ${low}"0000.V.pgm" $even

image = 0
while [ $image -le ((images/2)) ]
do
    _odd=(($image*2+1))
    ln -s $low$(printf "%04d.Y.pgm" $_odd) $odd$(printf "%04d.Y.pgm" $image)
    ln -s $low$(printf "%04d.U.pgm" $_odd) $odd$(printf "%04d.U.pgm" $image)
    ln -s $low$(printf "%04d.V.pgm" $_odd) $odd$(printf "%04d.V.pgm" $image)

    _even=(($image*2+1))
    ln -s $low$(printf "%04d.Y.pgm" $_even) $even$(printf "%04d.Y.pgm" $image)
    ln -s $low$(printf "%04d.U.pgm" $_even) $even$(printf "%04d.U.pgm" $image)
    ln -s $low$(printf "%04d.V.pgm" $_even) $even$(printf "%04d.V.pgm" $image)

    ((image++))
done
