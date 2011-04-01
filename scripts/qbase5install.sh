set -ex

while [ $# -gt 0 ]
do
  case $1
  in
    --hg-prefix)
      HG_PREFIX="$2"
      shift 2
    ;;

    *)
      echo "The arguments to use are"
      echo "--hg-prefix: The prefix to use for hg if you do not want to clone from bitbucket"
    ;;
  esac
done

if [ "${HG_PREFIX}" == "" ]; then
	HG_PREFIX="https://bitbucket.org"
fi

ARAKOON_DEB="arakoon_tip_amd64.deb"
ARAKOON_EGG="arakoon-tip_-py2.6.egg"
THRIFT_BDIST_VERSION="0.5.0"
THRIFT_BDIST="Thrift-${THRIFT_BDIST_VERSION}.linux-x86_64.tar.gz"
CONCURRENCE_BDIST_VERSION="0.3.1"
CONCURRENCE_BDIST="concurrence-${CONCURRENCE_BDIST_VERSION}.linux-x86_64.tar.gz"
POSIX_IPC_BDIST_VERSION="0.9.0"
POSIX_IPC_BDIST="posix_ipc-${POSIX_IPC_BDIST_VERSION}.linux-x86_64.tar.gz"
WGET="wget -nv "
# NOTE: Leave this var on one line, the hudson job greps it out to provide its local mirror
APT_PACKAGES="python2.6 mc python-openssl ejabberd python-pycurl python-pygresql mercurial wget ipython python-epydoc python-cheetah python-twisted python-setuptools postgresql-8.4 rabbitmq-server python-amqplib nginx python-yaml python-pyrex python-greenlet libevent-1.4-2"

apt-get install ${APT_PACKAGES} -y


cd /tmp
rm -f opt.tar.gz
rm -f "${ARAKOON_DEB}"
rm -f "${ARAKOON_EGG}"
rm -f "${THRIFT_BDIST}"

${WGET} http://fileserver.incubaid.com/pylabs5/opt.tar.gz
${WGET} "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/arakoon/tip/arakoon_tip_amd64.deb" -O "${ARAKOON_DEB}"
${WGET} "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/python-arakoon/tip/arakoon-tip_-py2.6.egg" -O "${ARAKOON_EGG}"
${WGET} "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/thrift/${THRIFT_BDIST_VERSION}/${THRIFT_BDIST}" -O "${THRIFT_BDIST}"
${WGET} "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/concurrence/${CONCURRENCE_BDIST_VERSION}/${CONCURRENCE_BDIST}" -O "${CONCURRENCE_BDIST}"
${WGET} "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/posix_ipc/${POSIX_IPC_BDIST_VERSION}/${POSIX_IPC_BDIST}" -O "${POSIX_IPC_BDIST}"

dpkg -i "${ARAKOON_DEB}"
easy_install "${ARAKOON_EGG}"

tar -xf opt.tar.gz
mkdir -p /opt

echo "Install thrift bdist: ${THRIFT_BDIST}"
cd /
tar -xvzf "/tmp/${THRIFT_BDIST}"
cd -

echo "Install concurrence bdist: ${CONCURRENCE_BDIST}"
cd /
tar -xvzf "/tmp/${CONCURRENCE_BDIST}"
cd -

echo "Install posix_ipc bdist: ${POSIX_IPC_BDIST}"
cd /
tar -xvzf "/tmp/${POSIX_IPC_BDIST}"
cd -

cp -rf opt/code/ /opt/
cp -rf opt/qbase5/ /opt/

cd /opt/code/incubaid/pylabs-core
hg pull -u "${HG_PREFIX}/incubaid/pylabs-core"

cd /opt/code/incubaid/qp5_-unstable-_pylabs5
hg pull -u "${HG_PREFIX}/incubaid/qp5_-unstable-_pylabs5"

cd /opt/code/incubaid/qp5_-unstable-_pylabs5_test
hg pull -u "${HG_PREFIX}/incubaid/qp5_-unstable-_pylabs5_test"

cd /opt/code/incubaid/qp5_-unstable-_qpackages5
hg pull -u "${HG_PREFIX}/incubaid/qp5_-unstable-_qpackages5"


mkdir -p /etc/python2.6
cp /opt/code/incubaid/pylabs-core/utils/system/sitecustomize.py /etc/python2.6/sitecustomize.py

ln -s /opt/code/incubaid/pylabs-core/apps/exampleapp /opt/qbase5/apps/pylabsExampleApp

cd /opt/code
hg clone --branch pylabs5 "${HG_PREFIX}/despiegk/pymodel" pymodel
hg clone --branch 0.5 "${HG_PREFIX}/despiegk/osis" osis
hg clone --branch pylabs5 "${HG_PREFIX}/despiegk/pylabs_workflowengine" workflowengine
hg clone --branch pylabs5 "${HG_PREFIX}/despiegk/pylabs_agent" pylabs_agent
hg clone "${HG_PREFIX}/despiegk/jswizards" jswizards
ln -s "`pwd`/pymodel/pymodel/" "/opt/qbase5/lib/python/site-packages/pymodel"
ln -s "`pwd`/osis/code/osis/" "/opt/qbase5/lib/python/site-packages/osis"
ln -s "`pwd`/workflowengine/workflowengine/lib/" "/opt/qbase5/lib/python/site-packages/workflowengine"
ln -s "`pwd`/workflowengine/workflowengine/manage/" "/opt/code/incubaid/pylabs-core/extensions/servers/workflowengine"
mkdir -p /opt/qbase5/apps/workflowengine/
ln -s "`pwd`/workflowengine/workflowengine/bin/" "/opt/qbase5/apps/workflowengine/bin"
ln -s "`pwd`/pylabs_agent/agent_service" "/opt/qbase5/lib/python/site-packages/"
mkdir -p /opt/qbase5/www
ln -s "`pwd`/jswizards" "/opt/qbase5/www"

hg clone "${HG_PREFIX}/despiegk/lfw" lfw
mkdir -p /opt/qbase5/www
ln -s "`pwd`/lfw/htdocs/" "/opt/qbase5/www/lfw"

echo "Symlink extra libs"
ln -s /opt/code/incubaid/pylabs-core/lib/* /opt/qbase5/lib/python/site-packages/

echo "Disable system postgres"
/etc/init.d/postgresql stop
update-rc.d -f postgresql remove

echo "Configure nginx"
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

EOF

echo "Setup done"
cd /opt/qbase5/apps/pylabsExampleApp
