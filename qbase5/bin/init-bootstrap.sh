
#set -e
curdir=`pwd`
base=/opt/qbase5

PATH=$base:$base/bin:$PATH

# Source all *.conf files in $base/init
for conffile in `find $base/init -type f -name '*.conf'`; do
  . ${conffile}
done