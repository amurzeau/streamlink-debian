#!/bin/sh

set -x

mkdir -p debian

wget -q https://raw.githubusercontent.com/amurzeau/streamlink-debian/master/debian/changelog -O debian/changelog &&
wget -q https://raw.githubusercontent.com/amurzeau/streamlink-debian/master/debian/watch -O debian/watch &&
! uscan --report-status
