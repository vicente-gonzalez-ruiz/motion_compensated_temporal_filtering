#! /bin/bash

echo $@ >> trace
$@
exit $?
