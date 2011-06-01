#!/bin/bash
set -e

UBUNTU_REPO=$1

echo "Generating en_US.UTF-8 locale"
locale-gen en_US.UTF-8

echo "Adding universe to sources.list"
cp /etc/apt/sources.list /etc/apt/sources.list.orig
echo "deb ${UBUNTU_REPO} maverick main universe" >> /etc/apt/sources.list

echo "Disabling recommended and suggested packages"
cat > /etc/apt/apt.conf.d/90local << EOF2
APT::Install-Recommends "0";
APT::Install-Suggests "0";
APT::Get::AllowUnauthenticated "1";
EOF2

echo "Updating apt"
apt-get -y update
echo "Installing wget"
apt-get install wget -y --force-yes


