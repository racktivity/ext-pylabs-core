#!/bin/bash
. ${WORKSPACE}/scripts/chroot/vars.sh
pushd ${WORKSPACE}/scripts/chroot
echo "Prepare chroot"
if [ ! -e $FULL_CLEAN_CHROOT_PATH ]; then
    . setup.sh
    . start.sh
elif
    . reset.sh    
fi
echo "Configure chroot"
sudo cp chroot_configure.sh "${FULL_CHROOT_PATH}/chroot_configure.sh"
sudo chmod u+x "${FULL_CHROOT_PATH}/chroot_configure.sh"
sudo chroot "${FULL_CHROOT_PATH}" "/chroot_configure.sh" "${UBUNTU_REPO}"
popd

echo "Prepare installer"
cd "${WORKSPACE}/scripts/installer"
mkdir -p "${WORKSPACE}/pylabs5"
./makeinstaller.sh "${WORKSPACE}/pylabs5-installer.sh"
echo "Launch installer"
sudo chmod u+x ${WORKSPACE}/pylabs5-install.sh
sudo cp "${WORKSPACE/pylabs5-install.sh}" "${FULL_CHROOT_PATH}/"
sudo chroot "${FULL_CHROOT_PATH}" "/pylabs5-install.sh"
