#!/bin/bash

# 更新YUM包索引并安装必要的包
yum install -y yum-utils device-mapper-persistent-data lvm2

# 添加Docker的官方YUM仓库
yum-config-manager --add-repo http://download.docker.com/linux/centos/docker-ce.repo

# 安装Docker CE
yum -y install docker-ce

# 添加docker用户组
groupadd docker 

# 将当前用户添加到docker组，这里使用root作为示例
gpasswd -a root docker 

#启动Docker服务
systemctl start docker

#令Docker服务自启
systemctl enable docker

# 下载指定版本的Docker Compose
curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 赋予Docker Compose执行权限
chmod +x /usr/local/bin/docker-compose

chmod +x back-end/boot.sh

# 显示Docker和Docker Compose的版本，确认安装成功
docker version
docker-compose version

# 确保elasticsearch数据目录权限
mkdir -p ./docker/elasticsearch/data
sudo chown -R 1000:1000 ./docker/elasticsearch/data

docker-compose up -d
