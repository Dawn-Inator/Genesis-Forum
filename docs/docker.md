<br>

# 目录导航

## 整体架构设计

### [Application Architecture](#application-architecture-1)

## Docker项目部署

### [Code Clone](#code-clone-1)

### [Docker Install](#docker-install-1)

### [DockerFile Create](#dockerfile-create-1)

- [Elasticsearch Create](#elasticsearch-createdeprecated-method)

- [Flask-api Create](#flask-api-dockerfile)

- [Nginx Create](#nginx-dockerfliedeprecated-method)

### [Docker-Compose Startup](#docker-compose-startup-1)

### [Bash in Onestep](#bash-in-onestep-1)

## 网站配置和SSL申请

### [Nginx Proxy Manager and SSL Configure](#nginx-proxy-manager-and-ssl-configure-1)

## 防火墙配置与部署错误处理

### [FireWall Configure and Chrome Error](./firewall.md)

<br><br>

# 整体架构设计

## Application Architecture
- front-end: vuejs开发，使用bootstrap UI框架
- back-end: flask开发

```

                               ---> (cdn代理)  
                               |        |
                               |        ↓
   Https ------> Cloudflare ---|--> (DNS 解析) ---------------------------> Chrome                
    ↑                          |        |    
    |                          |    (域名专属)   
    |                          |        ↓
    |                          --> Turnstile --(人机挑战)--  
    |                                                     |
    |                                                     |
    -------(加密)--------- 云主机 -------> Docker          |           
             ↑               ↑               |            |                   
             |               |               |            |
         (SSL证书)       (端口映射)       (镜像构建)        |    
             |               |               ↓            |
   ----------|---------------|----------------------------|--------------------------
   |         |               |                            |                         |
   |         |           (流量输出)                        |                         |
   |         |               |                            |                         |
   |  Nginx Proxy Manager-----                            |                         |
   |         |                                            ↓                         |                  
   |         |             --> Nginx ---(静态代理)---> front-end                     |                   
   |         |             |                              |                         |                   
   |         |             |                              |                         |                 
   |         ---(web代理)---                            axios(连接前后端)            |                   
   |                       |                              |                         |
   |                       |                              |                         |                
   |                       --> Gunicorn --(进程代理)-- back-end                      |
   |                                                      |                         |                
   |                                                    (连接)                      |
   |                                                      |                         |
   |                                     -----------------|-----------------        |
   |                                     |                |                |        |
   |                                 (数据存储)       (搜索 功能)        (缓存系统)   |
   |                                     |                |                |        |
   |                                   MySQL        Elasticsearch        Redis      |
   |                                                                                |
   ----------------------------------------------------------------------------------

```

<br>

- docker镜像原理
- Dockerfile是镜像配置，镜像可生成1个或者多个容器
```
                             --------> 容器1
                             |
docker --(Dockerfile)--> docker镜像 
                             |
                             --------> 容器2

```

- 前后端一键启动思路(以后端api为例)
```                           

                  -------(bash启动命令)------
                  |                         |    
                  |                         ↓
docker --(Dockerfile.flask)--> api镜像 --(CMD启动)--> api容器
  |                               ↑
  |                               |
  ----------(代码复制)-------------                

```

- 所以配置docker-compose.yml时
- 对于MySQL，Redis等使用官方默认的镜像的，不需要Dockerfile配置
- 对于Elasticsearch因为要自定义下载ik插件，需要Dockerfile配置
- 对于前后端既要配置代码，又要自定义启动，需要Dockerfile和bash.sh共同完成

<br><br>

# Docker项目部署

## Code Clone
- 路径放在 /home/www/
```
cd /home/

mkdir www&&cd www

git clone https://github.com/Dawn-Inator/Genesis-Forum.git -b linux
```

## App Configure
- 修改前端配置
```
vim front-end/src/http.js
```

```
if (process.env.NODE_ENV === 'production') {
  axios.defaults.baseURL = 'http://x.x.x.x:5000';
} else {
  axios.defaults.baseURL = 'http://127.0.0.1:5000';
}
```

- 修改后端配置
- 因为后端有时读不到docker的环境变量，所以我们直接写入后端
```
vim back-end/config.py
```

```
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 日志输出到控制台还是日志文件中
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'false').lower() in ['true', 'on', '1']
    
    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = 1
    MAIL_USERNAME='服务器的qq邮箱'
    MAIL_PASSWORD='qq邮箱的授权码'
    MAIL_SENDER='发送者的名字'
    ADMINS = ['admin_1@qq.com','admin_2@qq.com']  # 管理员的邮箱地址
    
    # 分页设置
    POSTS_PER_PAGE = 10
    USERS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 10
    MESSAGES_PER_PAGE = 10
    TASKS_PER_PAGE = 10
    # Redis 用于 RQ 任务队列
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    # Elasticsearch 全文检索
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or '127.0.0.1:9200'
    # Flask-Babel
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    LANGUAGES = ['zh', 'en']
```

- 获取cloudflare授权码
- 修改 front-end/src/components/Auth/login.vue
- 完成之后可触发人机挑战
```
vim front-end/src/components/Auth/login.vue
```

```
 data () {
    return {
      cf_token: '',
      cf_sitekey: '你的cloudflare授权码',
      sharedState: store.state,
      loginForm: {
        username: '',
        password: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        usernameError: null,
        passwordError: null
      }
    }
  },
```

## Docker Install
*Docker 镜像存储在本地系统目录的文件里面，我们的基础目录选择在/www/Genesis-Forum/下*

安装docker
```
yum install -y yum-utils device-mapper-persistent-data lvm2

yum-config-manager --add-repo http://download.docker.com/linux/centos/docker-ce.repo

yum -y install docker-ce
```

- 给docker赋权
```
sudo groupadd docker 

sudo gpasswd -a root docker 

sudo service docker restart 
```

- 启动docker并自启
```
systemctl start docker

systemctl enable docker
```

## DockerFile Create
- 镜像配置我们一般放在/www/Genesis-Forum/下
- cd /home/www/Genesis-Forum/

### ~~Elasticsearch Create(Deprecated Method)~~
- **方法过于复杂，已弃用**
  - 由于我们的代码中使用了 ik 分词器，所以需要在 Elasticsearch 官方提供的镜像中先安装 ik，再保存为修改后的镜像
  - 启动容器
  
        docker pull docker.elastic.co/elasticsearch/elasticsearch:7.0.0

        docker run -d \
          --name elasticsearch \
          -p 9200:9200 \
          -p 9300:9300 \
          -e "discovery.type=single-node" \
          -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \
          docker.elastic.co/elasticsearch/elasticsearch:7.0.0



  - 安装 IK 分词器
  - docker exec 命令允许你在运行中的容器内执行命令。-it 选项组合是为了开启一个交互式的 tty 终端，使你能够直接与容器内的命令行交互。elasticsearch 是目标容器的名称或 ID，/bin/bash 是你希望在容器内执行的命令，这里是启动 bash shell。
    
        docker exec -it elasticsearch /bin/bash

        elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.0.0/elasticsearch-analysis-ik-7.0.0.zip

        exit

  - 保存为新的镜像，删除旧容器

        docker commit elasticsearch my-elasticsearch-ik

        docker rm -f elasticsearch 


### Elasticsearch Create(Recommended Method)
- 推荐方法
- 构建elasticsearch的镜像配置

```
vim Dockerfile.elasticsearch
```

```
FROM docker.elastic.co/elasticsearch/elasticsearch:7.0.0

RUN elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.0.0/elasticsearch-analysis-ik-7.0.0.zip
```

- 后来的安装设置已经整合到docker-compose.yml里面了

### Flask-api Dockerfile
- 配置gunicorn
- "-"意味着让Gunicorn将访问日志和错误日志输出到标准输出流（stdout）和标准错误流（stderr）。这种配置在Docker容器环境中非常有用，因为它允许日志被容器化应用的默认日志收集机制捕获，而不是写入到文件中。这样，您可以通过docker logs命令或者Docker的日志驱动来收集和查看日志，方便在容器化部署中的日志管理和监控。
```
vim back-end/gunicorn.conf.py
```
  
```
import multiprocessing

bind = '0.0.0.0:5000'
workers = multiprocessing.cpu_count() * 2 + 1
loglevel = 'info'
accesslog = "-"
errorlog = "-"
```

- 新建启动脚本，因为有多条命令，不方便直接写到 Dockerfile.flask 中的 CMD 子命令中
```
vim back-end/boot.sh
```

```
#!/bin/bash

while true; do
    flask db upgrade
    if [ "$?" == "0" ]; then
        break
    fi
    echo "Failed to apply the migration to the database, retrying in 3 secs..."
    sleep 3
done
flask deploy
exec gunicorn startup:app -c gunicorn.conf.py
```
- 授予可执行权限
```
chmod +x back-end/boot.sh
```

- 然后再新建一个 Dockerfile.flask
- WORKDIR设置容器内部的工作目录为/app，这不是linux主机的路径
- COPY将linux主机路径./back-end复制到docker容器路径/app
```
vim Dockerfile.flask
```

```
FROM python:3.7.4

WORKDIR /app

COPY ./back-end /app

RUN chmod +x /app/boot.sh

RUN pip install -r requirements.txt && pip install pymysql gunicorn pyopenssl

ENV FLASK_APP startup.py

EXPOSE 5000

ENTRYPOINT ["bash", "/app/boot.sh"]
```

- 构建后端 Flask API 镜像(可选)，已经整合到docker-compose.yml里面了
- -f 或 --file 参数指定了构建镜像时使用的 Dockerfile 文件的路径，在这个例子中，Dockerfile 位于 back-end 目录下
- -t 或 --tag 参数用于给构建的镜像指定一个标签，格式通常是 `<name>:<tag>`
- 使用 . 表示当前目录作为构建上下文发送给 Docker 守护进程
```
docker build -f Dockerfile.flask -t flask-api:1.0.0 .
```

### ~~Nginx Dockerflie(Deprecated Method)~~
- **方法过于复杂，已弃用**
  - 首先宿主机安装 Node.js，我们通过 Node Version Manager（简称，nvm）来安装指定版本
  - 加载 .bash_profile 文件，其中包含初始化 NVM 环境所需的路径和变量

        curl https://raw.githubusercontent.com/creationix/nvm/v0.13.1/install.sh | bash

        source ~/.bash_profile

        nvm list-remote

        nvm install v10.15.3

        node --version


  - 生成静态文件

        cd front-end

        npm install

        npm run build

        mkdir -p ../docker/nginx/data

        cp -a dist/* ../docker/nginx/data

        cd ..


### Nginx Dockerflie(Recommended Method)
- 配置启动脚本
```
vim front-end/boot.sh
```

```
#!/bin/bash

# 复制静态文件
cp -r /app/dist/* /usr/share/nginx/html/

# 启动 Nginx
exec nginx -g 'daemon off;'
```

- 配置镜像文件
```
vim Dockerfile.nginx
```

```
# 第一阶段：使用 Node.js 镜像构建静态文件
FROM node:10.15.3 AS builder

# 设置工作目录
WORKDIR /app

# 复制前端源代码到工作目录
COPY ./front-end /app

# 安装依赖并构建静态文件
RUN npm install && npm run build

# 第二阶段：使用 Nginx 镜像
FROM nginx:latest

# 将从第一阶段构建的整个 app 目录（包括 dist）复制到 Nginx 镜像中的 /app 下
COPY --from=builder /app /app

# 暴露端口
EXPOSE 80

RUN chmod +x /app/boot.sh

ENTRYPOINT ["bash", "/app/boot.sh"]
```

- 然后整合到了docker-compose.yml里面了

## Docker-Compose Startup
*在单机上可以使用 Docker Compose 来编排我们多个容器，只需要提供一个 YML 配置文件，一条命令就可以把这些容器全部启动起来，非常方便*

- Linux 安装 Docker-CE 时，默认没有安装 Compose 工具，需要我们额外安装
```
curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose

docker-compose --version

> docker-compose version 1.24.0, build 0aa59064
```

- 或者通过 Python3 下的 pip3 工具安装
```
pip3 install docker-compose

ln -s /usr/local/python-3.7/bin/docker-compose /usr/local/bin/docker-compose
```

- 配置docker-compose.yml
- 可以使用 `docker-compose config` 命令检查有没有语法错误
- www/Genesis-Forum/
```
vim docker-compose.yml
```

```
version: "3.7"
services:

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=Password_123456
      - MYSQL_DATABASE=forum
      - MYSQL_USER=testuser
      - MYSQL_PASSWORD=Password_123456
    ports:
      - "3306:3306"
    volumes:
      - "./docker/mysql/conf.d:/etc/mysql/conf.d"
      - "./docker/mysql/data:/var/lib/mysql"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - "./docker/redis/data:/data"
    command: redis-server --appendonly yes

  elasticsearch:
    build:
      context: . 
      dockerfile: Dockerfile.elasticsearch
    user: "1000:1000"
    environment:
      - "discovery.type=single-node"
      - "ES_JAVA_OPTS=-Xms256m -Xmx256m"
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - "./docker/elasticsearch/data:/usr/share/elasticsearch/data"

  flask-api:
    build:
      context: .   
      dockerfile: Dockerfile.api  
    image: flask-api:1.0.0   # 指定构建完成的镜像名和标签
    environment:
      - REDIS_URL=redis://redis:6379/0
      - ELASTICSEARCH_URL=elasticsearch:9200
      - DATABASE_URL=mysql+pymysql://testuser:Password_123456@mysql:3306/forum
    ports:
      - "5000:5000"

  rq-worker:
    image: flask-api:1.0.0
    environment:
      - DATABASE_URL=mysql+pymysql://testuser:Password_123456@mysql/forum
      - REDIS_URL=redis://redis:6379/0
      - ELASTICSEARCH_URL=elasticsearch:9200
    entrypoint: rq
    command: worker -u redis://redis:6379/0 flask-tasks

  nginx:
    build:
      context: . 
      dockerfile: Dockerfile.nginx
    image: nginx-vuejs
    ports:
      - "8080:80"
      - "8443:443"
    volumes:
      - "./docker/nginx/data:/usr/share/nginx/html"

  nginx-proxy-manager:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ./docker/npm/data:/data
      - ./docker/npm/letsencrypt:/etc/letsencrypt
      
```

- 启动所有容器，'-d' 选项表示在后台运行 compose，否则在前台输出日志
- ps查看容器状态
```
docker-compose up -d

docker-compose ps
```

- logs查看各容器的运行日志，'-f' 选项持续输出
- 后面加容器名字可以查看指定容器
```
docker-compose logs 

docker-compose logs flask-api
```

- 停止全部容器
- 或者删除指定容器
```
docker-compose stop

docker-compose rm flask-api
```

- 操作容器内部
- 如nginx，这样可以进入nginx内部的命令行
```
docker-compose exec nginx bash
```

- 如果你修改了配置或代码，可以重新构建镜像并运行容器
```
docker-compose build

docker-compose up -d
```

## Bash in Onestep
- 将cmd命令压缩成一个文件
- 一键安装docker和启动服务
- 于/Genesis-Forum/创建onestep.sh
```
vim onestep.sh
```

```
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
```

<br><br>

# 网站配置和SSL申请

## Nginx Proxy Manager and SSL Configure
***Nginx Proxy Manager可以代理应用并管理域名和网站流量，也可以一步申请SSL证书，使用的是Let's encryt的证书*** 

- 当docker容器跑起来后， 连接到81端口即可访问管理界面。访问：http://你的服务器IP:81
- 第一次登录的默认管理员账户：
```
Email:    admin@example.com
Password: changeme
```

- 第一次登陆后，你会立刻被要求修改登录密码和一些重要信息。
- 然后进行应用代理，添加ssl证书
```
代理端口如下:

Nginx: 8080

flask-api: 5000

nginx-proxy-manager:81
```

<br><br>

# 防火墙配置与部署错误处理

## FireWall Configure and Chrome Error

- 接下来记得配置防火墙
- 具体详情点击[这里](firewall.md)

---