#! /bin/bash

## Add a final symbol.
function end {
    (echo -e "" >&2)
    # (echo -n "[1;0m" >&2)
    exit
}

# (echo -en "[0;32m" >&2)

if [ -z "$*" ]; then
    (echo -e "" >&2)
    (echo -e "+-------------+" >&2)
    (echo -e "| MCTF parser |" >&2)
    (echo -e "+-------------+" >&2)
    (echo -e "" >&2)
    (echo -e MCTF=\"$MCTF\" >&2)
    (echo -e "" >&2)
    (echo -e "Available commands:" >&2)
    (echo -e "" >&2)
    ls $MCTF/bin
    (echo -e "" >&2)
    (echo -e "Type: \n\n mctf command --help \n\nto get information about the command line parameters" >&2)
    end
fi

echo `pwd` - "$MCTF/bin/$@"
echo "$MCTF/bin/$@" >> trace
#set -x
"$MCTF/bin/$@"
#set +x
exit $?

# (echo -en "[1;0m" >&2)
