#!/bin/bash

set -e

. vars.sh

read -p "HG username: " HG_USERNAME
read -s -p "HG password: " HG_PASSWORD && echo

sudo cp chroot_install.sh "${FULL_CHROOT_PATH}/chroot_install.sh"
sudo cp chroot_configure.sh "${FULL_CHROOT_PATH}/chroot_configure.sh"
sudo chmod u+x "${FULL_CHROOT_PATH}/chroot_install.sh"
sudo chmod u+x "${FULL_CHROOT_PATH}/chroot_configure.sh"
sudo chroot "${FULL_CHROOT_PATH}" "/chroot_configure.sh" "${UBUNTU_REPO}"
sudo chroot "${FULL_CHROOT_PATH}" "/chroot_install.sh" --hg-username "${HG_USERNAME}" --hg-password "${HG_PASSWORD}"
