#!/bin/bash
set -e
. ${WORKSPACE}/scripts/chroot/vars.sh
pushd ${WORKSPACE}/scripts/chroot
echo "Prepare chroot"
if [ ! -e $FULL_CLEAN_CHROOT_PATH ]; then
    . setup.sh
    . start.sh
else
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
mkdir -p "${WORKSPACE}/testresults"
./makeinstaller.sh "${WORKSPACE}/pylabs5-installer.sh"
echo "Launch installer"
sudo chmod u+x ${WORKSPACE}/pylabs5-installer.sh
sudo cp "${WORKSPACE}/pylabs5-installer.sh" "${FULL_CHROOT_PATH}/"
sudo chroot "${FULL_CHROOT_PATH}" /pylabs5-installer.sh --bootstrap-package sampleapp
echo "Run tests"
sudo cp -a "${WORKSPACE}/test" ${FULL_CHROOT_PATH}/opt/qbase5/mytests
cat > "/tmp/mytest.sh" << EOF
#!/bin/bash
/opt/qbase5/qshell -c "p.application.install('awingu')"
cd /opt/qbase5/mytests/
nosetests --with-xunit -v
EOF
sudo cp /tmp/mytest.sh "${FULL_CHROOT_PATH}/mytest.sh"
sudo chmod +x "${FULL_CHROOT_PATH}/mytest.sh"
sudo chroot "${FULL_CHROOT_PATH}" apt-get install -y python-nose
sudo chroot "${FULL_CHROOT_PATH}" /mytest.sh || true
sudo cp -a "${FULL_CHROOT_PATH}/opt/qbase5/mytests/"*.xml ${WORKSPACE}/testresults/

