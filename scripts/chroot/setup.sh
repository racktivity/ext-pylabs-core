#!/bin/bash

set -e

echo "Including vars"
. vars.sh

if [ -e "${FULL_CHROOT_PATH}" ]; then
	echo "Cannot setup your chroot, the full chroot path ${FULL_CHROOT_PATH} already exists";
fi

echo "Installing deboostrap"
sudo apt-get install debootstrap -y
echo "Creating a clean sandbox in ${FULL_CHROOT_PATH}"
sudo debootstrap --arch=amd64 maverick "${FULL_CHROOT_PATH}" "http://archive.ubuntu.com/ubuntu/"
echo "Backing up the clean sandbox to ${FULL_CLEAN_CHROOT_PATH}"
sudo cp -R "${FULL_CHROOT_PATH}" "${FULL_CLEAN_CHROOT_PATH}"

echo "You are good to go! Just run start.sh and then install.sh to get you up and running"
