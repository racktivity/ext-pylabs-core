#!/bin/bash
set -e

CORE_PACKAGES="ipython python-pkg-resources mercurial python-apt curl"

log () {
    if test "x$TERM" == "xunknown"; then
        echo $@
    else
        echo -e "\033[1m"$@"\033[0m"
    fi
}

check_system_version () {
    log "Checking if your system version is Ubuntu 10.10 Maverick"
    LSB_RELEASE="$(lsb_release -c | cut -f 2)"
    if [ "${LSB_RELEASE}" != "maverick" ]; then
        log "Your system version is not Ubuntu 10.10 Maverick";
        exit 1
    else
        log "Your system is Ubuntu 10.10 Maverick. The install can continue."
    fi
}


self_extract(){
    log "Extracting base layout"
    ARCHIVE=$(awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }' $0)
    mkdir -p /opt
    tail -n+$ARCHIVE $0 | tar xz -C /opt
}

get_qbase_remote(){
    TARFILE=/tmp/installer.$$
    curl http://qpackage.racktivity.com/bundles/installer/qbase5.tgz > $TARFILE
    tar xf $TARFILE -C /opt
    rm $TARFILE
}

install_qbase(){
    if [ ! -e $0 ]; then
        get_qbase_remote
        return
    fi
    SIZE=$(stat -c %s $0)
    if [ $SIZE -gt 102400 ]; then
        self_extract
    else
        get_qbase_remote
    fi
}

customize(){
    log "Adding sitecustomize to system python"
    mkdir -p /etc/python2.6
    cp /opt/qbase5/utils/system/sitecustomize.py /etc/python2.6/sitecustomize.py
}

update_metadata(){
    log "Updating Q-Package metadata"
    /opt/qbase5/qshell -c "i.qp.updateMetaDataAll()"
}

configure_packages(){
    log "Configuring Q-Packages"
    /opt/qbase5/qshell -c "q.qp._runPendingReconfigeFiles()"
}

install_qpackage(){
    packagename=$1
    log "Installing Q-Package ${packagename}"
    /opt/qbase5/qshell -c "i.qp.find('${packagename}').install()"
    configure_packages
}

install_package(){
    local packages
    packages=$1
    log "Installing ${packages}"
    apt-get install -qq -y $packages > /dev/null
}

apt_update(){
  apt-get update
}

core_install(){
    apt_update
    install_package "${CORE_PACKAGES}"
    install_qbase
    customize
    update_metadata
    install_qpackage pylabs
}

usage(){
    echo "Usage $0"
    echo "  --bootstrap-package: The Q-Package you want to install by default, default pyapps_framework"
    exit 1
}
BOOTSTRAP_PACKAGE="pyapps_framework"

while [ $# -gt 0 ]
do
  case $1
  in
    --bootstrap-package)
      BOOTSTRAP_PACKAGE="$2"
      shift 2
    ;;


    *)
      usage
    ;;
  esac
done

check_system_version
core_install

if [ -n ${BOOTSTRAP_PACKAGE}  ]; then
    install_qpackage ${BOOTSTRAP_PACKAGE}
fi

exit 0
__ARCHIVE_BELOW__
