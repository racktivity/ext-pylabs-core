#!/bin/bash

# NOTE: Leave this var on one line, the hudson job greps it out to provide its local mirror
APT_PACKAGES="python2.6 python-openssl ejabberd python-pycurl python-pygresql mercurial wget ipython python-epydoc python-cheetah python-twisted python-setuptools postgresql-8.4 rabbitmq-server python-amqplib nginx python-yaml python-pyrex python-greenlet libevent-1.4-2 python-sqlalchemy python-psycopg2 python-paramiko python-apt"

# Package versions
THRIFT_BDIST_VERSION="0.5.0"
CONCURRENCE_BDIST_VERSION="0.3.1"
POSIX_IPC_BDIST_VERSION="0.9.0"

ARAKOON_DEB="arakoon_tip_amd64.deb"
ARAKOON_EGG="arakoon-tip_-py2.6.egg"

# These use version information defined above, don't change unless required
THRIFT_BDIST="Thrift-${THRIFT_BDIST_VERSION}.linux-x86_64.tar.gz"
CONCURRENCE_BDIST="concurrence-${CONCURRENCE_BDIST_VERSION}.linux-x86_64.tar.gz"
POSIX_IPC_BDIST="posix_ipc-${POSIX_IPC_BDIST_VERSION}.linux-x86_64.tar.gz"


TMP_DIR="/tmp/qbase5install"
ROOT_DIR="/"
QBASE_DIR="/opt/qbase5"

my_log () {
    if test "x$TERM" == "xunknown"; then
        echo $@
    else
        echo -e "\033[1m"$@"\033[0m"
    fi
}

check_system_version () {
    my_log "Checking if your system version is Ubuntu 10.10 Maverick"
    LSB_RELEASE="$(lsb_release -c | cut -f 2)"
    if [ "${LSB_RELEASE}" != "maverick" ]; then
	    my_log "Your system version is not Ubuntu 10.10 Maverick";
	    exit 1
    else
	    my_log "Your system is Ubuntu 10.10 Maverick. The install can continue."
    fi
}

my_wget () {
    local cmd

    my_log "Retrieving $1"
    cmd="wget -nv $1"
    echo $cmd
    $cmd || my_die "wget failed"
    echo
}

my_apt_get () {
    local cmd

    my_log "Running apt-get"
    cmd="apt-get $@"
    echo $cmd
    $cmd || my_die "apt-get failed"
    echo
}

my_dpkg () {
    local cmd

    my_log "Running dpkg"
    cmd="dpkg $@"
    echo $cmd
    $cmd || my_die "dpkg failed"
    echo
}

my_easy_install () {
    local cmd

    my_log "Running easy_install"
    cmd="easy_install $@"
    echo $cmd
    $cmd || my_die "easy_install failed"
    echo
}

my_hg () {
    local cmd

    my_log "Running Mercurial client"
    cmd="hg $@"
    if [ "x${HG_PASSWORD}" != "x" ]; then
        echo "${cmd//${HG_PASSWORD}/***}"
    else
        echo "${cmd}"
    fi
    $cmd || my_die "hg failed"
    echo
}

my_tar () {
    local cmd

    my_log "Unpacking Tar archive"
    cmd="tar $@"
    echo $cmd
    $cmd || my_die "tar failed"
    echo
}

my_die () {
    echo
    if test "x$TERM" == "xunknown"; then
        echo "Error:" $@
    else
        echo -e '\E[31m\033[1m'Error: $@'\033[0m'
        tput sgr0
    fi
    echo

    exit 1
}

my_check_command () {
    which $@ > /dev/null || my_die "Command $@ not found"
}

set -e

check_system_version

while [ $# -gt 0 ]
do
  case $1
  in
    --hg-username)
      HG_USERNAME="$2"
      shift 2
    ;;

    --hg-password)
      HG_PASSWORD="$2"
      shift 2
    ;;

    --hg-prefix)
      HG_PREFIX="$2"
      shift 2
    ;;

    *)
      echo "The arguments to use are"
      echo "--hg-username: Your bitbucket username"
      echo "--hg-password: Your bitbucket password"
      echo "--hg-prefix: The prefix to use for hg if you do not want to clone from bitbucket, username and password are ignored if you use hg-prefix"
      exit 1
    ;;
  esac
done

if ! test "x${TERM}" == "xunknown"; then
    clear
fi

if [ "x${HG_PREFIX}" == "x" ]; then
	if [ "x${HG_USERNAME}" != "x" ]; then
		HG_PREFIX="https://${HG_USERNAME}:${HG_PASSWORD}@bitbucket.org"
	else
		echo "Either provide an HG prefix or HG username and password"
		exit 1
	fi
fi

my_log "Cleaning system"
my_log "Removing ${QBASE_DIR}"
rm -rf "${QBASE_DIR}"
my_log "Removing /opt/code"
rm -rf /opt/code
my_log "Removing ${TMP_DIR}"
rm -rf "${TMP_DIR}"

my_log "Starting installation"

my_apt_get install -y ${APT_PACKAGES}

my_log "Checking system dependencies"
my_check_command wget
my_check_command apt-get
my_check_command dpkg
my_check_command hg
my_check_command tar
my_check_command python
my_check_command easy_install
my_check_command update-rc.d

mkdir -p $TMP_DIR
pushd $TMP_DIR

my_log "Retrieving sandbox image"
rm -f opt.tar.gz
my_wget http://fileserver.incubaid.com/pylabs5/opt.tar.gz

my_log "Retrieving Arakoon server package"
rm -f "${ARAKOON_DEB}"
my_wget "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/arakoon/tip/arakoon_tip_amd64.deb" -O "${ARAKOON_DEB}"

my_log "Retrieving Arakoon Python client package"
rm -f "${ARAKOON_EGG}"
my_wget "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/python-arakoon/tip/arakoon-tip_-py2.6.egg" -O "${ARAKOON_EGG}"

my_log "Retrieving Thrift Python package"
rm -f "${THRIFT_BDIST}"
my_wget "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/thrift/${THRIFT_BDIST_VERSION}/${THRIFT_BDIST}" -O "${THRIFT_BDIST}"

my_log "Retrieving Concurrence Python package"
rm -f "${CONCURRENCE_BDIST}"
my_wget "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/concurrence/${CONCURRENCE_BDIST_VERSION}/${CONCURRENCE_BDIST}" -O "${CONCURRENCE_BDIST}"

my_log "Retrieving Posix IPC Python package"
rm -f "${POSIX_IPC_BDIST}"
my_wget "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/posix_ipc/${POSIX_IPC_BDIST_VERSION}/${POSIX_IPC_BDIST}" -O "${POSIX_IPC_BDIST}"

my_log "Installing Arakoon server package"
my_dpkg -i "${ARAKOON_DEB}"
my_log "Installing Arakoon Python client package"
my_easy_install "${ARAKOON_EGG}"

popd

pushd $ROOT_DIR
my_log "Install Thrift Python package"
my_tar -xvzf "${TMP_DIR}/${THRIFT_BDIST}"
popd

pushd $ROOT_DIR
my_log "Install Concurrence Python package"
my_tar -xvzf "${TMP_DIR}/${CONCURRENCE_BDIST}"
popd

pushd $ROOT_DIR
my_log "Install POSIX IPC Python package"
my_tar -xvzf "${TMP_DIR}/${POSIX_IPC_BDIST}"
popd

pushd ${TMP_DIR}
my_log "Unpacking sandbox image"
my_tar -xf opt.tar.gz
mkdir -p /opt
my_log "Moving code folder to /opt/code"
mv opt/code /opt/
my_log "Moving qbase5 folder to /opt/qbase5"
mv opt/qbase5 /opt/
popd

my_log "Removing leftover log files"
rm -rf "${QBASE_DIR}/var/log"
mkdir -p "${QBASE_DIR}/var/log"

my_log "Creating QShell startup files"
mkdir -p ${QBASE_DIR}/init
touch ${QBASE_DIR}/init/ipy_user_conf.py

my_log "Updating Mercurial repositories"

pushd /opt/code/incubaid/pylabs-core
my_hg pull -u "${HG_PREFIX}/incubaid/pylabs-core"
popd

pushd /opt/code/incubaid/qp5_-unstable-_pylabs5
my_hg pull -u "${HG_PREFIX}/incubaid/qp5_-unstable-_pylabs5"
popd

pushd /opt/code/incubaid/qp5_-unstable-_pylabs5_test
my_hg pull -u "${HG_PREFIX}/incubaid/qp5_-unstable-_pylabs5_test"
popd

pushd /opt/code/incubaid/qp5_-unstable-_qpackages5
my_hg pull -u "${HG_PREFIX}/incubaid/qp5_-unstable-_qpackages5"
popd

my_log "Configuring system Python"
mkdir -p /etc/python2.6
cp /opt/code/incubaid/pylabs-core/utils/system/sitecustomize.py /etc/python2.6/sitecustomize.py

#TODO Do we want this?
my_log "Installing Pylabs Example application"
ln -sf /opt/code/incubaid/pylabs-core/apps/exampleapp /opt/qbase5/apps/pylabsExampleApp

#link macro documentation in sampleapp doc
ln -s /opt/code/lfw/docs/alkiradocs /opt/qbase5/apps/pyapps/sampleapp/portal/spaces

pushd /opt/code
my_log "Cloning repositories"
my_hg clone --branch pylabs5 "${HG_PREFIX}/despiegk/pymodel" pymodel
my_hg clone --branch 0.5 "${HG_PREFIX}/despiegk/osis" osis
my_hg clone --branch pylabs5 "${HG_PREFIX}/despiegk/pylabs_workflowengine" workflowengine
my_hg clone --branch pylabs5 "${HG_PREFIX}/despiegk/pylabs_agent" pylabs_agent
my_hg clone "${HG_PREFIX}/despiegk/jswizards" jswizards
my_hg clone --branch default "${HG_PREFIX}/despiegk/lfw" lfw

my_log "Creating symlinks to repositories in ${QBASE_DIR}"
ln -s "`pwd`/pymodel/pymodel/" "/opt/qbase5/lib/python/site-packages/pymodel"
ln -s "`pwd`/osis/code/osis/" "/opt/qbase5/lib/python/site-packages/osis"

ln -s "`pwd`/workflowengine/workflowengine/lib/" "/opt/qbase5/lib/python/site-packages/workflowengine"
ln -s "`pwd`/workflowengine/workflowengine/manage/" "/opt/code/incubaid/pylabs-core/extensions/servers/workflowengine"
mkdir -p /opt/qbase5/apps/workflowengine/
ln -s "`pwd`/workflowengine/workflowengine/bin/" "/opt/qbase5/apps/workflowengine/bin"

ln -s "`pwd`/pylabs_agent/agent_service" "/opt/qbase5/lib/python/site-packages/"

mkdir -p /opt/qbase5/www
ln -s "`pwd`/jswizards" "/opt/qbase5/www"
#TODO Do we want this?
ln -s "`pwd`/jswizards/libs" "/opt/qbase5/www/js"
ln -s "`pwd`/lfw/htdocs/" "/opt/qbase5/www/lfw"
ln -s "`pwd`/lfw/services/lfw/lfw.py" "/opt/qbase5/lib/python/site-packages/"

my_log "Creating symlinks to extra libraries"
ln -s /opt/code/incubaid/pylabs-core/lib/* /opt/qbase5/lib/python/site-packages/

my_log "Disable system PostgreSQL service"
test -x /etc/init.d/postgresql && /etc/init.d/postgresql stop
update-rc.d -f postgresql remove

my_log "Configuring nginx"
python << EOF
from pylabs.InitBase import q

PORT = 80
PATH = 'static'
ROOT = '/opt/qbase5/www'

nginx = q.manage.nginx

nginx.startChanges()

cmdb = nginx.cmdb

if str(PORT) not in cmdb.virtualHosts:
    cmdb.addVirtualHost(str(PORT), port=PORT)

vhost = cmdb.virtualHosts[str(PORT)]

if PATH not in vhost.sites:
    site = vhost.addSite(PATH, '/%s' % PATH)
    site.addOption('root', ROOT)
    site.addOption('rewrite ', '^/%s/(.*) /\$1 break' % PATH)
    site.addOption('rewrite  ', '^/%s$ /%s/ permanent' % (PATH, PATH))

nginx.save()
nginx.applyConfig()

q.extensions.enable('q.clients.arakoon')
EOF

my_log "Setup done"
