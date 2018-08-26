#!/bin/bash
#install dotnet && supervisor

#安装目录
INSTALL_DIR=/etc
SRC_DIR=$PWD

[ ! -d ${INSTALL_DIR} ] && mkdir -p ${INSTALL_DIR}
#[ ! -d ${SRC_DIR} ] && mkdir -p ${SRC_DIR}

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script!!"
    exit 1
fi

#安装依赖包
rpm -Uvh https://packages.microsoft.com/config/rhel/7/packages-microsoft-prod.rpm
for Package in wget gcc gcc-c++ make autoconf automake  python-setuptools python3 
do
    yum -y install $Package
done

 wget -qO- https://raw.github.com/ma6174/vim/master/setup.sh | sh -x
