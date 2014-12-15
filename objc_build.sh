#!/bin/bash

if [ ! -n "$1" ]
then
	echo "Usage: `basename $0` Source CompileName"
	exit 0
fi

gcc `gnustep-config --objc-flags` $1 -o $2 -L /GNUstep/System/Library/Libraries -lobjc -lgnustep-base
