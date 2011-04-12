#!/bin/bash

set -e

echo "Including vars"
. vars.sh
echo "Stopping chroot"
. stop.sh

echo "Cleaning up old chroot and copying the clean chroot"
sudo rm -Rf "${FULL_CHROOT_PATH}"
sudo cp -R "${FULL_CLEAN_CHROOT_PATH}" "${FULL_CHROOT_PATH}"

echo "Starting in new chroot"
. start.sh
