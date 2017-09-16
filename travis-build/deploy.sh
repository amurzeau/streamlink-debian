#!/bin/bash

bintray_repository="${1:-debian}"
CHROOT_DIST=${1:-stable}
CHROOT_ARCH=amd64
CHROOT_NAME=$CHROOT_DIST-$CHROOT_ARCH-sbuild

echo "Deploying on bintray repository $bintray_repository"

CHROOT_SESSION=$(sudo schroot -c "${CHROOT_NAME}" --begin-session)
sudo schroot --run-session -c $CHROOT_SESSION -u root -- apt-get install -y --no-install-recommends python3 python3-debian python3-requests
sudo -E schroot -p --run-session -c $CHROOT_SESSION -u $USER -- python3 $(dirname "$0")/bintray_upload_changes.py amurzeau $bintray_repository $CHROOT_DIST *.changes
sudo schroot --end-session -c $CHROOT_SESSION
