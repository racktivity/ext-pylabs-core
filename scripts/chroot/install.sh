#!/bin/bash

. vars.sh

sudo cp /srv/chroot/chroot_install.sh "${FULL_CHROOT_PATH}/chroot_install.sh"
sudo chown u+x "${FULL_CHROOT_PATH}/chroot_install.sh"
sudo chroot "${FULL_CHROOT_PATH}" "/chroot_install.sh"
