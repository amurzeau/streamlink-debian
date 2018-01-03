#!/bin/sh

set -x

mkdir -p debian

wget -q https://raw.githubusercontent.com/amurzeau/streamlink-debian/master/debian/changelog -O debian/changelog &&
wget -q https://raw.githubusercontent.com/amurzeau/streamlink-debian/master/debian/watch -O debian/watch &&
# uscan on travis does not support version 4
sed -i 's/version=4/version=3/' debian/watch &&
! uscan --report-status
