#!/bin/bash

set -xe

CHROOT_DIST=unstable
CHROOT_ARCH=amd64
CHROOT_NAME=$CHROOT_DIST-$CHROOT_ARCH-sbuild
CHROOT_DEBIAN_MIRROR=http://ftp.de.debian.org/debian/
CHROOT_ADDITIONAL_PACKETS=gnupg,lintian,sbuild,schroot

# Install dependencies on ubuntu to create a chroot with debian unstable
sudo apt-get install -y --no-install-recommends git-buildpackage dpkg-dev schroot sbuild debootstrap

# Build source package (build errors will be found early)
git-buildpackage --git-verbose --git-ignore-branch

# Create debian unstable chroot
mkdir ~/chroot
sudo sbuild-createchroot --arch=$CHROOT_ARCH $CHROOT_DIST ~/chroot/$CHROOT_NAME/ $CHROOT_DEBIAN_MIRROR --keyring= --include=$CHROOT_ADDITIONAL_PACKETS ||
(cat ~/chroot/$CHROOT_NAME/debootstrap/debootstrap.log && exit 2)

# Configure schroot
sudo bach -c "echo 'union-type=overlayfs' >> /etc/schroot/chroot.d/$CHROOT_NAME*"
cat /etc/schroot/chroot.d/$CHROOT_NAME*
cp travis-build/sbuild-key.* /var/lib/sbuild/apt-keys/

# Configure mounts inside first schroot
sudo bash -c "echo '/home/$USER  /home/$USER none  rw,bind 0       0' >> /etc/schroot/sbuild/fstab"
sudo bash -c "echo '/var/lib/schroot /var/lib/schroot none  rw,bind 0       0' >> /etc/schroot/sbuild/fstab"

# Configure mounts inside build schroot
sudo mkdir -p ~/chroot/$CHROOT_NAME/etc/schroot/chroot.d/
sudo bash -c "echo '/home/$USER  /home/$USER none  rw,bind 0       0' >> ~/chroot/$CHROOT_NAME/etc/schroot/sbuild/fstab"
sudo cp /etc/schroot/chroot.d/$CHROOT_NAME* ~/chroot/$CHROOT_NAME/etc/schroot/chroot.d/
sudo sed -i 's/script-config=.*/profile=sbuild/' ~/chroot/$CHROOT_NAME/etc/schroot/chroot.d/$CHROOT_NAME*

SESSION=$(schroot --begin-session -c $CHROOT_NAME)
echo $SESSION
schroot --run-session -c "$SESSION" -u root -- sbuild-adduser $USER
schroot --run-session -c "$SESSION" -- sbuild -As ../*.dsc -d $CHROOT_DIST --run-lintian
schroot --end-session -c "$SESSION"

