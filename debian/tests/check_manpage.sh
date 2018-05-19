#!/bin/sh

set -xe

echo "Checking man page $1"
man "$1" > /dev/null 2>&1
