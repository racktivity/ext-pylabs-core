#!/bin/bash

. vars.sh

for i in /sys /dev /tmp /proc /dev/pts; do sudo mount -o bind "${i}" "${FULL_CHROOT_PATH}/${i}"; done
sudo cp /etc/hosts "${FULL_CHROOT_PATH}/etc/hosts"

sudo cp /srv/chroot/install.sh "${FULL_CHROOT_PATH}/install.sh"
sudo chmod u+x "${FULL_CHROOT_PATH}/install.sh"

