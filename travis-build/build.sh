#!/bin/bash

set -xe

CHROOT_DIST=unstable
CHROOT_ARCH=amd64
CHROOT_NAME=$CHROOT_DIST-$CHROOT_ARCH-sbuild
CHROOT_DEBIAN_MIRROR=http://ftp.de.debian.org/debian/
CHROOT_ADDITIONAL_PACKETS="gnupg lintian sbuild schroot"

# Install dependencies on ubuntu to create a chroot with debian unstable
sudo apt-get install -y --no-install-recommends git-buildpackage dpkg-dev schroot sbuild debootstrap

# Build source package (build errors will be found early)
git-buildpackage --git-verbose --git-ignore-branch '--git-builder=dpkg-source -b .' --git-cleaner=

# Add _apt user so debian unstable schroot won't warn about missing user _apt
id -u _apt > /dev/null 2>&1 || sudo adduser --force-badname --system --home /nonexistent --no-create-home --quiet _apt || true

# Create debian unstable chroot
mkdir ~/chroot
sudo sbuild-createchroot --arch=$CHROOT_ARCH $CHROOT_DIST ~/chroot/$CHROOT_NAME/ $CHROOT_DEBIAN_MIRROR --keyring= || (cat ~/chroot/$CHROOT_NAME/debootstrap/debootstrap.log && exit 2)

# Fix _apt permissions
sudo chown -R _apt:root ~/chroot/$CHROOT_NAME/var/lib/apt/lists/partial || true

# Configure schroot
sudo bash -c "echo 'union-type=overlayfs' >> /etc/schroot/chroot.d/$CHROOT_NAME*"
cat /etc/schroot/chroot.d/$CHROOT_NAME*
sudo cp travis-build/sbuild-key.* /var/lib/sbuild/apt-keys/
sudo bash -c "echo '/home/$USER  /home/$USER none  rw,bind 0       0' >> /etc/schroot/sbuild/fstab"
sudo bash -c "echo '/var/lib/schroot /var/lib/schroot none  rw,bind 0       0' >> /etc/schroot/sbuild/fstab"
sudo schroot -c "source:${CHROOT_NAME}" -u root -d / -- apt-get install -y --no-install-recommends $CHROOT_ADDITIONAL_PACKETS

# Configure mounts inside schroot
sudo mkdir -p ~/chroot/$CHROOT_NAME/etc/schroot/chroot.d/
sudo bash -c "echo '/home/$USER  /home/$USER none  rw,bind 0       0' >> ~/chroot/$CHROOT_NAME/etc/schroot/sbuild/fstab"
sudo cp /etc/schroot/chroot.d/$CHROOT_NAME* ~/chroot/$CHROOT_NAME/etc/schroot/chroot.d/
sudo sed -i 's/script-config=.*/profile=sbuild/' ~/chroot/$CHROOT_NAME/etc/schroot/chroot.d/$CHROOT_NAME*

# Add current user to sbuild group (required by sbuild)
sudo sbuild-adduser $USER

sudo schroot -c "$CHROOT_NAME" -u $USER -- sbuild -As ../*.dsc -d $CHROOT_DIST --run-lintian
