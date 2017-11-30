/*! \file vshow.sh

    \brief Displays a sequence.

    \author Vicente Gonzalez-Ruiz.
    \date Last modification: 2015, January 7.
*/

set -x
mplayer $1 -demuxer rawvideo -rawvideo w=352:h=288 -loop 0 -fps $2 > /dev/null 2> /dev/null &
set +x

