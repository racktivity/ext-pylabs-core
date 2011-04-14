#!/bin/bash

CORE_PACKAGES="ipython python-pkg-resources mercurial"

self_extract(){
    echo "Exctracting base layout"
    ARCHIVE=$(awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }' $0)
    mkdir -p /opt
    tail -n+$ARCHIVE $0 | tar xz -C /opt
}

customize(){
    echo "Adding sitecustomize to system python"
    mkdir -p /etc/python2.6
    cp /opt/qbase5/utils/system/sitecustomize.py /etc/python2.6/sitecustomize.py    
}

install_packages(){
    local packages
    packages=$1
    echo "Installing ${packages}"
    apt-get install -qq -y $packages > /dev/null
}

install(){
    self_extract
    install_packages "${CORE_PACKAGES}"
    customize
}

install
exit 0
__ARCHIVE_BELOW__
