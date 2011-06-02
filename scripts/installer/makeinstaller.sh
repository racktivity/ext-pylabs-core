#!/bin/bash

set -e

SCRIPTDIR=$(readlink -f $(dirname $0))
REPOPATH=$(readlink -f "${SCRIPTDIR}/../..")
TFOLDER="/tmp/$(basename $0).$$.tmp"
QBASE="${TFOLDER}/qbase5"
TARFILE=$(readlink -f "$1")

mkdir -p "${QBASE}/apps"
for app in applicationserver cloud_api_generator; do
    cp -a "${REPOPATH}/apps/${app}" "${QBASE}/apps/${app}"
done

cp -a ${REPOPATH}/qbase5/* "${QBASE}/"
#mkdir "${QBASE}/init"
#touch "${QBASE}/init/ipy_user_conf.py"

mkdir -p "${QBASE}/lib/python2.6/site-packages"
mkdir -p "${QBASE}/lib/python"
mkdir -p "${QBASE}/lib/pylabs/core"

cp -a "${REPOPATH}/core" "${QBASE}/lib/pylabs/core/pylabs"
cp -a "${REPOPATH}/extensions" "${QBASE}/lib/pylabs/extensions"
cp -a "${REPOPATH}/lib" "${QBASE}/lib/python/site-packages"

mkdir -p "${QBASE}/pyapps"

cp -a "${REPOPATH}/utils" "${QBASE}/utils"

mkdir -p ${QBASE}/var/{cmdb,log,pid}

touch ${TARFILE}

if [ -z "$2" ]; then
    cat "${SCRIPTDIR}/installscript.sh" > ${TARFILE}
fi
pushd ${TFOLDER}
tar czf - . >> ${TARFILE}
popd

chmod +x ${TARFILE}
rm -rf ${TFOLDER}

echo "Tar created at ${TARFILE}"
