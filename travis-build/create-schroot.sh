#!/bin/sh

set -x

CHROOT_DIST=${1:-stable}
CHROOT_ARCH=amd64
CHROOT_NAME=$CHROOT_DIST-$CHROOT_ARCH-sbuild
CHROOT_DEBIAN_MIRROR=http://ftp.de.debian.org/debian/
CHROOT_LOCATION=${2:-"~/chroot/$CHROOT_NAME/"}

apt-get install -y --no-install-recommends schroot sbuild debootstrap

# Add _apt user so debian schroot won't warn about missing user _apt
id -u _apt > /dev/null 2>&1 || sudo adduser --force-badname --system --home /nonexistent --no-create-home --quiet _apt || true

sbuild-createchroot --arch=$CHROOT_ARCH $CHROOT_DIST $CHROOT_LOCATION $CHROOT_DEBIAN_MIRROR --keyring= || (cat $CHROOT_LOCATION/debootstrap/debootstrap.log && exit 2)

# Fix _apt permissions
chown -R _apt:root $CHROOT_LOCATION/var/lib/apt/lists/partial || true
