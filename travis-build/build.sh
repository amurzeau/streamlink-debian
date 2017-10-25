#!/bin/bash

set -xe

SCRIPT_DIR=$(dirname "$0")

CHROOT_DIST=${1:-stable}
CHROOT_ALIAS=$2
CHROOT_TARGET_DIST=${CHROOT_ALIAS:-$CHROOT_DIST}
CHROOT_ARCH=amd64
CHROOT_NAME=$CHROOT_DIST-$CHROOT_ARCH-sbuild
CHROOT_DEBIAN_MIRROR=http://ftp.de.debian.org/debian/
CHROOT_COMMON_ADDITIONAL_PACKETS="sbuild schroot gnupg lintian autopkgtest dpkg-dev git-buildpackage pristine-tar"

STABLE_CHROOT_NAME=stable-$CHROOT_ARCH-sbuild
STABLE_CHROOT_LOCATION=~/chroot/stable

TARGET_CHROOT_LOCATION=~/chroot/$CHROOT_DIST

# Create debian stable chroot
mkdir -p ~/chroot
if [ ! -d $STABLE_CHROOT_LOCATION ]; then
	sudo "$SCRIPT_DIR/create-schroot.sh" stable "$STABLE_CHROOT_LOCATION"

	# Configure schroot
	sudo bash -c "echo 'union-type=overlayfs' >> /etc/schroot/chroot.d/$STABLE_CHROOT_NAME*"
	sudo bash -c "echo '/home/$USER  /home/$USER none  rw,bind 0       0' >> /etc/schroot/sbuild/fstab"
	sudo bash -c "echo '/var/lib/schroot /var/lib/schroot none  rw,bind 0       0' >> /etc/schroot/sbuild/fstab"
	sudo schroot -c "source:${STABLE_CHROOT_NAME}" -u root -d / -- apt-get install -y --no-install-recommends ${CHROOT_COMMON_ADDITIONAL_PACKETS}

	cat /etc/schroot/chroot.d/$STABLE_CHROOT_NAME*
fi

# Add current user to sbuild group (required by sbuild)
sudo sbuild-adduser $USER

CHROOT_SESSION=$(sudo schroot -c "${STABLE_CHROOT_NAME}" --begin-session)
sudo schroot --run-session -c $CHROOT_SESSION -u root -- "$SCRIPT_DIR/create-schroot.sh" $CHROOT_DIST $TARGET_CHROOT_LOCATION
if [ -n "$CHROOT_ALIAS" ]; then
	sudo schroot --run-session -c $CHROOT_SESSION -u root -- bash -c "echo 'aliases=$CHROOT_ALIAS' >> /etc/schroot/chroot.d/$CHROOT_NAME*"
fi
sudo schroot --run-session -c $CHROOT_SESSION -u root -- bash -c "sed -i 's/union-type=.*/union-type=overlay/' /etc/schroot/chroot.d/$CHROOT_NAME*"
sudo schroot --run-session -c $CHROOT_SESSION -u root -- bash -c "echo '/home/$USER  /home/$USER none  rw,bind 0       0' >> /etc/schroot/sbuild/fstab"
sudo schroot --run-session -c $CHROOT_SESSION -u root -- bash -c "cat /etc/schroot/chroot.d/$CHROOT_NAME*"

# git-buildpackage does not work with trusty linux kernel, rename syscall fail if target already exists
sudo schroot --run-session -c $CHROOT_SESSION -u root -- bash -c "patch /usr/lib/python2.7/dist-packages/gbp/scripts/buildpackage.py < $SCRIPT_DIR/buildpackage.py.patch"
sudo schroot --run-session -c $CHROOT_SESSION -u $USER -- gbp buildpackage --git-verbose --git-ignore-branch --git-cleaner= "--git-builder=sbuild -v -As -d $CHROOT_DIST --no-clean-source --run-lintian --lintian-opts=\"-EviIL +pedantic\" --run-autopkgtest --autopkgtest-root-args= --autopkgtest-opts=\"-- schroot %r-%a-sbuild\""
sudo schroot --end-session -c $CHROOT_SESSION

ls -l build-dir
cat build-dir/*.changes
