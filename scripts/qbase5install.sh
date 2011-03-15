set -ex
apt-get install python2.6 mc python-openssl python-pycurl python-pygresql mercurial wget ipython python-epydoc -y

cd /tmp
rm -f opt.tar.gz
wget http://files.incubaid.com/pub/opt.tar.gz

tar -xf opt.tar.gz
mkdir -p /opt

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

cd /opt/qbase5/apps/pylabsExampleApp

