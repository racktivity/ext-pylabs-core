set -ex
ARAKOON_DEB="arakoon_0.9.0-1_amd64.deb"
ARAKOON_EGG="arakoon-0.9.0-1-py2.6.egg"
THRIFT_BDIST_VERSION="0.5.0"
THRIFT_BDIST="Thrift-${THRIFT_BDIST_VERSION}.linux-x86_64.tar.gz"
# NOTE: Leave this var on one line, the hudson job greps it out to provide its local mirror
APT_PACKAGES="python2.6 mc python-openssl python-pycurl python-pygresql mercurial wget ipython python-epydoc python-cheetah python-twisted python-setuptools postgresql-8.4 rabbitmq-server python-amqplib nginx"

apt-get install ${APT_PACKAGES} -y


cd /tmp
rm -f opt.tar.gz
rm -f "${ARAKOON_DEB}"
rm -f "${ARAKOON_EGG}"
rm -f "${THRIFT_BDIST}"

wget http://fileserver.incubaid.com/pylabs5/opt.tar.gz
wget "http://confluence.incubaid.com/download/attachments/2326551/arakoon_0.9.0-1_amd64.deb" -O "${ARAKOON_DEB}"
wget "http://confluence.incubaid.com/download/attachments/2326551/arakoon-0.9.0-1-py2.6.egg" -O "${ARAKOON_EGG}"
wget "http://fileserver.incubaid.com/pylabs5/qpackages/pylabs5/thrift/${THRIFT_BDIST_VERSION}/${THRIFT_BDIST}" -O "${THRIFT_BDIST}"

dpkg -i "${ARAKOON_DEB}"
easy_install "${ARAKOON_EGG}"

tar -xf opt.tar.gz
mkdir -p /opt

echo "Install thrift bdist: ${THRIFT_BDIST}"
cd /
tar -xvzf "/tmp/${THRIFT_BDIST}"
cd -

cp -rf opt/code/ /opt/
cp -rf opt/qbase5/ /opt/

cd /opt/code/incubaid/pylabs-core
hg pull -u

cd /opt/code/incubaid/qp5_-unstable-_pylabs5
hg pull -u

cd /opt/code/incubaid/qp5_-unstable-_pylabs5_test
hg pull -u

cd /opt/code/incubaid/qp5_-unstable-_qpackages5
hg pull -u


mkdir -p /etc/python2.6
cp /opt/code/incubaid/pylabs-core/utils/system/sitecustomize.py /etc/python2.6/sitecustomize.py

ln -s /opt/code/incubaid/pylabs-core/apps/exampleapp /opt/qbase5/apps/pylabsExampleApp

cd /opt/code
hg clone --branch pylabs5 https://bitbucket.org/despiegk/pymodel pymodel
hg clone --branch 0.5 https://bitbucket.org/despiegk/osis osis
ln -s "`pwd`/pymodel/pymodel/" "/opt/qbase5/lib/python/site-packages/pymodel"
ln -s "`pwd`/osis/code/osis/" "/opt/qbase5/lib/python/site-packages/osis"

echo "Disable system postgres"
/etc/init.d/postgresql stop
update-rc.d -f postgresql remove

echo "Setup done"
cd /opt/qbase5/apps/pylabsExampleApp
