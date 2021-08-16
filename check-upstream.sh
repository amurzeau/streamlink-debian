#!/bin/sh

set -x

mkdir -p debian debian/upstream

wget https://raw.githubusercontent.com/amurzeau/streamlink-debian/master/debian/changelog -O debian/changelog &&
wget https://raw.githubusercontent.com/amurzeau/streamlink-debian/master/debian/watch -O debian/watch &&
wget https://raw.githubusercontent.com/amurzeau/streamlink-debian/master/debian/upstream/signing-key.asc -O debian/upstream/signing-key.asc &&
! uscan --report-status
