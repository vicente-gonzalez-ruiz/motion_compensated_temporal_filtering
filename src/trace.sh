#! /bin/bash


## \file trace.sh
#
#  \brief Register to a log file.
#
#  \author Vicente Gonzalez-Ruiz.
#  \date Last modification: 2015, January 7.

echo $@ >> trace
$@
exit $?
