#!/bin/bash

set -e

. vars.sh

for i in /sys /dev /tmp /proc ; do sudo mount -o rbind "${i}" "${FULL_CHROOT_PATH}/${i}"; done
sudo cp /etc/hosts "${FULL_CHROOT_PATH}/etc/hosts"
