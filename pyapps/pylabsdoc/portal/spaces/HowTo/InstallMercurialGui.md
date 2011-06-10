## Install the Mercurial GUI: hgtk

Only applies for Ubuntu 9.1

topmenu > system > administration > software sources > add
or manually
add the source to you apt sources in etc

add:
[[code]]
deb http://ppa.launchpad.net/tortoisehg-ppa/stable-snapshots/ubuntu karmic main 
#or for ubuntu 10.10
deb http://ppa.launchpad.net/tortoisehg-ppa/stable-snapshots/ubuntu maverick main 
[[/code]]

[[code]]
apt-get install tortoisehg-nautilus
[[/code]]

install iniparse
[[code]]
cd /tmp
wget http://iniparse.googlecode.com/files/iniparse-0.4.tar.gz
tar -xzf iniparse-0.4.tar.gz 
mkdir /usr/lib/pymodules/python2.6
cp iniparse-0.4/iniparse/* /usr/lib/pymodules/python2.6/iniparse/
[[/code]]


hgtk userconfig
fill in user, difftools, ...
type hgtk in you bash shell

more info see 
* https://launchpad.net/~tortoisehg-ppa/+archive/stable-snapshots
* https://bitbucket.org/tortoisehg/stable/wiki/hgtk



