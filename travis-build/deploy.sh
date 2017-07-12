#!/bin/bash

bintray_repository="${1:-debian}"

echo "Deploying on bintray repository $bintray_repository"

CHROOT_SESSION=$(sudo schroot -c "unstable-amd64-sbuild" --begin-session)
sudo schroot --run-session -c $CHROOT_SESSION -u root -- apt-get install -y --no-install-recommends python3 python3-debian python3-requests
sudo -E schroot -p --run-session -c $CHROOT_SESSION -u $USER -- python3 $(dirname "$0")/bintray_upload_changes.py amurzeau $bintray_repository *.changes
sudo schroot --end-session -c $CHROOT_SESSION
