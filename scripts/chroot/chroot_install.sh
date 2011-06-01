#!/bin/bash

set -e

SCRIPT_NAME="qbase5install.sh"
HG_USERNAME=""
HG_PASSWORD=""

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

    *)
      echo "The arguments to use are"
      echo "--hg-username: The hg username to clone from bitbucket"
      echo "--hg-password: The hg password to clone from bitbucket"
      exit 1
    ;;
  esac
done

echo "HG_USERNAME is ${HG_USERNAME}"

if [ "${HG_USERNAME}" == "" ]; then
	echo "Please provide a hg username with --hg-username";
	exit 2
fi

if [ "${HG_PASSWORD}" == "" ]; then
	echo "Please provide a hg password with --hg-password";
	exit 3
fi

echo "Installing Pylabs 5"
cd /opt
rm -f ${SCRIPT_NAME}
wget --no-check-certificate --no-cache "https://bitbucket.org/incubaid/pylabs-core/raw/default/scripts/${SCRIPT_NAME}" -O ${SCRIPT_NAME}
chmod u+x ${SCRIPT_NAME}
./${SCRIPT_NAME} --hg-username "${HG_USERNAME}" --hg-password "${HG_PASSWORD}"

echo "Symlinking our sample app"
mkdir -p /opt/qbase5/pyapps/
ln -s /opt/code/incubaid/pylabs-core/pyapps/sampleapp/ /opt/qbase5/pyapps/sampleapp
