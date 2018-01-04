#!/bin/sh

set -x

mkdir -p debian debian/upstream

wget -q https://raw.githubusercontent.com/amurzeau/streamlink-debian/master/debian/changelog -O debian/changelog &&
wget -q https://raw.githubusercontent.com/amurzeau/streamlink-debian/master/debian/watch -O debian/watch &&
wget -q https://raw.githubusercontent.com/amurzeau/streamlink-debian/master/debian/upstream/signing-key.asc -O debian/upstream/signing-key.asc &&
# uscan on travis does not support version 4
sed -i 's/version=4/version=3/' debian/watch &&
! uscan --report-status
