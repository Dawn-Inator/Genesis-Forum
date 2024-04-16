<br>

# 目录导航

## 整体架构设计

### [Application Architecture](#application-architecture-1)

## 论坛应用本体配置

### [Code Clone](#code-clone-1)

### [Flask Configure](#flask-configure-1)

### [Vuejs Configure](#vuejs-configure-1)

### [Cloudflare Configure](#cloudflare-configure-1)

## 搭建环境组件配置

### [Mysql Install](#mysql-install-1)

### [Redis Install](#redis-install-1)

### [Elasticsearch Install](#elasticsearch-install-1)

### [Python Install](#python-install-1)

### [Gunicorn Install](#gunicorn-install-1)

### [Supervisor Install](#supervisor-install-1)

### [Nginx Install](#nginx-install-1)

## SSL证书配置 (可选)

### [Apply for an SSL Certificate](#apply-for-an-ssl-certificate-1)

### [Upload to Nginx Server](#upload-to-nginx-server-1)

### [Upload to Gunicorn Server](#upload-to-gunicorn-server-1)

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
         Https ------> Cloudflare ---|--> (DNS 解析) -----------------> Chrome                
          ↑                 |        |        |    
          |                 |        |    (域名专属)   
          |                 |        |        ↓
        (加密)<--(SSL证书)---         --> Turnstile --(人机挑战)     
          |                                               |                   
          |                                               ↓
          |               Nginx  -------(代理)-------> front-end 
          |                 |                             |                                          
          ------------------|                          axios(连接前后端)    
                            |                             |                
  Supervisor --(监听)--> Gunicorn -------(代理)------> back-end 
                                                          |                                      
                                                        (连接)                      
                                                          |                         
                                         -----------------|-----------------        
                                         |                |                |        
                                     (数据存储)       (搜索 功能)        (缓存系统)   
                                         |                |                |        
                                       MySQL        Elasticsearch        Redis      
                                     
```

<br>

- 前后端原理
```
    前端主机                                          后端主机
       ↓                                                 ↓
  [front-end]               ---------(返回结果)----- [back-end]
       |                    |                             ↑
       |                    ↓                             |
       --(告诉后端ip)--> [Chrome] --(根据ip请求或发送数据)---

```
- 由上图可知Chrome要同时处理front-end和back-end的数据流量，所以https加密的ssl证书需要分别部署front-end和back-end
- 我们只是将前端主机和后端主机合二为一，但是用axios连接时依然要写全ip地址x.x.x.x:5000，让Chrome知道去哪里获取数据

```
       --------------------主机---------------------------
       |                                                 |
       ↓                                                 ↓
  [front-end]               ---------(返回结果)----- [back-end]
       |                    |                             ↑
       |                    ↓                             |
       --(告诉后端ip)--> [Chrome] --(根据ip请求或发送数据)---

```

<br><br>

# 论坛应用本体配置

## Code Clone
- 路径放在 /home/www/
```
cd /home/

mkdir www&&cd www

git clone https://github.com/Dawn-Inator/Genesis-Forum.git -b linux
```

## Flask Configure
- 修改.env配置文件 
- /home/www/Genesis-Forum/back-end/.env 
```
cd /home/www/Genesis-Forum/back-end/

vim .env
```

```
FLASK_APP=startup.py
FLASK_DEBUG=0
FLASK_COVERAGE=1

ADMINS='<管理者的邮箱1>,<管理者的邮箱1>'

MAIL_SERVER='smtp.qq.com'
MAIL_PORT=465
MAIL_USE_SSL=1
MAIL_USERNAME='<服务器的qq邮箱>'
MAIL_PASSWORD='<qq邮箱的授权码>'
MAIL_SENDER='<发送者的名字>'

REDIS_URL='redis://127.0.0.1:6379/0'
ELASTICSEARCH_URL='127.0.0.1:9200'
```
- 如果不加这一句则使用sqlite环境，不用安装mysql
- 搭建好mysql环境后再加这一句进.env
```
DATABASE_URL=mysql+pymysql://testuser:Password_123456@localhost:3306/forum
```

- venv进入python虚拟环境，并安装flask的依赖插件(需先搭建python环境)
- /home/www/Genesis-Forum/back-end/
```
python3 -m venv venv3

source venv3/bin/activate

pip3 install -r requirements.txt
```

- 尝试启动 Flask 应用查看是否能ping通 (需先搭建MySQL环境) 
```
flask db upgrade

flask deploy

flask run -h 0.0.0.0 -p 5000
```

- 在笔记本中打开浏览器，访问 http://x.x.x.x:5000/api/ping
- 如果返回 "Pong!" 则说明正常，先停止应用
---
- 后台挂起命令 (可选)
```
nohup flask run -h 0.0.0.0 -p 5000 > flask.log &
```
- 查看进程
- a: 显示所有用户的进程，而不仅仅是当前用户的进程。
- u: 以用户为主要显示方式来显示详细信息，例如进程的所有者、进程 ID (PID)、CPU 使用率、内存使用率等。
- x: 显示不受控制终端控制的所有进程，即显示后台进程。
```
ps aux | grep flask
```

- 杀死进程
```
kill -9 PID
```

## Vuejs Configure
- 先修改 /home/www/Genesis-Forum/front-end/src/http.js，指定后端 API 的地址为 Linux 服务器 IP
```
if (process.env.NODE_ENV === 'production') {
  axios.defaults.baseURL = 'http://x.x.x.x:5000';
} else {
  axios.defaults.baseURL = 'http://127.0.0.1:5000';
}
```
- 如果你想使用https加密，记得替换即可
- 或者连接域名
```
if (process.env.NODE_ENV === 'production') {
  axios.defaults.baseURL = 'https://api.com';
} else {
  axios.defaults.baseURL = 'http://127.0.0.1:5000';
}
```

- 将前端代码打包成正式环境运行所需的静态文件
```
yum install npm

npm install

npm run build
```

- 新生成的dist文件夹后面的 Nginx 要用

- 可以修改webpack模组：config/index.js 文件内将`127.0.0.1`改为`0.0.0.0`，这样笔记本可以通过`x.x.x.x:8080`访问页面。但是笔记本不能连接后端服务器，会有跨域报错，浏览器出于安全考虑阻止了这个请求。
```
> Access to XMLHttpRequest at 'http://x.x.x.x:5000/api/tokens' from origin 'http://x.x.x.x:8080' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

- 我们将会使用Nginx来解决安全问题

<br><br>

## Cloudflare Configure
- 修改 /home/www/Genesis-Forum/front-end/src/components/Auth/login.vue
- 完成之后可触发人机挑战
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

# 搭建环境组件配置

## MySQL Install
***MySQL作为数据库管理存储数据***

- 安装 MySQL 社区版，我们使用MySQL 8.0的版本
- 使用 wget 命令下载 MySQL 社区版发行包的 RPM 文件。这个包不包含MySQL数据库软件本身，而是包含了安装MySQL所需的仓库信息。
- yum repolist enabled查看可以安装的软件版本，我们检查mysql安装包是否是8.0
```
wget https://dev.mysql.com/get/mysql80-community-release-el7-11.noarch.rpm

yum install  mysql80-community-release-el7-11.noarch.rpm

yum repolist enabled | grep mysql
```

- 如果直接yum install进行安装，会出现提示获取GPG密钥失败
- 我们需要导入密钥 https://repo.mysql.com/RPM-GPG-KEY-mysql-2022 注意，这个链接可能会随着时间更改，最好去官网进行检查
- 然后检查mysql80-community-release-el7-11.noarch.rpm
- 成功后安装
```
rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022

rpm --checksig mysql80-community-release-el7-11.noarch.rpm

> mysql80-community-release-el7-6.noarch.rpm: rsa sha1 (md5) pgp md5 确定

sudo yum -y  install mysql-community-server
```

- 启动mysql并令其自启
```
systemctl start mysqld

systemctl enable mysqld
```

- 查看初始密码并修改，我们将root密码修改为 Password_123456
- root用户只能从localhost这个ip登录账号
```
grep 'temporary password' /var/log/mysqld.log

> A temporary password is generated for root@localhost: xxxxxxxx

mysql -uroot -p

> Enter password: xxxxxxxx

ALTER USER 'root'@'localhost' IDENTIFIED BY 'Password_123456';
```

- 然后创建forum这个数据库
- 指定了数据库的字符集为 utf8mb4。utf8mb4 是 UTF-8 编码的超集，支持存储任意 Unicode 字符。这使得数据库能够存储多种语言的文本而不会出现乱码。
```
CREATE DATABASE forum
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

- 我们开始创建testuser用户密码也是Password_123456
- 之后back-end将使用该用户连接mysql
```
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'Password_123456';

GRANT ALL ON forum.* TO 'testuser'@'localhost';

FLUSH PRIVILEGES;

quit;
```
- MySQL的部分已经完成了

## Redis Install
***Redis用作缓存系统，后端应用会使用 RQ 任务队列，它需要 Redis***

- 安装epel-release(Extra Packages for Enterprise Linux)可以添加 EPEL 仓库到系统的仓库列表中，从而使得用户能够安装那些在yum默认仓库中不可用的软件包。
```
yum install -y epel-release
```

- 从epel-release中用yum安装redis
- enable能使程序自启
```
yum install -y redis

systemctl start redis   

systemctl enable redis  
```

## Elasticsearch Install
***Elasticsearch提供全文检索功能***

- 需要java 8驱动
```
yum -y install java-1.8.0-openjdk
```

- 导入 Elasticsearch GPG 公钥到 RPM 包管理系统中，用于确保从 Elasticsearch 官方仓库下载的软件包是未经篡改的
```
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
```

- 在yum仓库创建elasticsearch的下载配置并安装
```
vim /etc/yum.repos.d/elasticsearch.repo
```

```
[elasticsearch-7.x]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```

- 注意我们安装的是elasticsearch 7.17.18版本
```
yum -y install elasticsearch-7.17.18
```

- 调整 Elasticsearch JVM参数，它默认会使用 1G 内存，我们改成256MB
```
vim /etc/elasticsearch/jvm.options
```

```
# Xms represents the initial size of total heap space
# Xmx represents the maximum size of total heap space

-Xms256m
-Xmx256m
```

- 安装analysis-ik插件：博文基本上是中文字符，使用 Elasticsearch 默认的词法分析器效果不好，所以需要安装 elasticsearch-analysis-ik
- 注意analysis-ik插件版本号需和elasticsearch的一致，我们是7.17.18
```
/usr/share/elasticsearch/bin/elasticsearch-plugin install https://github.com/infinilabs/analysis-ik/releases/download/v7.17.18/elasticsearch-analysis-ik-7.17.18.zip
```

- 验证安装插件是否成功
```
ls /usr/share/elasticsearch/plugins

> analysis-ik

/usr/share/elasticsearch/bin/elasticsearch-plugin list

> analysis-ik
```

- 启动
```
systemctl start elasticsearch.service

systemctl enable elasticsearch.service
```

## Python Install
- 准备编译环境
```
yum -y install gcc make readline-devel sqlite-devel openssl openssl-devel libffi-devel zlib*
```

- 编译安装
```
wget http://python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz

tar xf Python-3.7.4.tar.xz

cd Python-3.7.4/

./configure --prefix=/usr/local/python-3.7

make && make install

rm -r /usr/bin/python3

rm -r /usr/bin/pip3

ln -s /usr/local/python-3.7/bin/python3.7 /usr/bin/python3

ln -s /usr/local/python-3.7/bin/pip3.7 /usr/bin/pip3

ln -s /usr/local/python-3.7/bin/pip3.7 /usr/bin/pip
```

## Gunicorn Install
***Gunicorn是一个 Python WSGI HTTP 服务器，Gunicorn 的工作模式（包括同步和异步工作者）允许它根据应用的需求和服务器的资源情况，高效地利用 CPU 和内存资源，通过预分配工作进程（workers）来并行处理多个请求，这提高了应用处理请求的能力，使其能够同时服务于多个客户端。这里我们用它来反向代理flask应用***
- 记得带venv3虚拟环境
```
pip install gunicorn
```

- 进行Gunicorn配置
- -w 3： 表示将启动 3 个 Gunicorn 进程，建议是 CPU 核数 * 2 + 1
- startup:app： 表示将要启动的应用为，当前目录下的 startup.py 模块中的 app 对象
- /home/www/Genesis-Forum/back-end/
```
vim gunicorn.conf.py
```

```
import multiprocessing

bind = '0.0.0.0:5000'
workers = multiprocessing.cpu_count() * 2 + 1
# daemon = True
pidfile = '/run/gunicorn.pid'
loglevel = 'info'
errorlog = '/tmp/gunicorn-error.log'
accesslog = '/tmp/gunicorn-access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
```

- 启动命令 (可选)
- /home/www/Genesis-Forum/back-end/
```
gunicorn startup:app -c gunicorn.conf.py
```

## Supervisor Install
***Supervisor 主要用于管理长时间运行的进程，用户可以轻松地启动、停止、重启和监视在 Supervisor 的控制下运行的进程，还能自动记录被管理进程的 stdout 和 stderr 输出，方便后期查看和调试。我们使用Supervisor来监管Gunicorn，把它放到 CentOS后台执行***
```
yum install -y supervisor

systemctl start supervisord.service

systemctl enable supervisord.service
```

- Supervisor配置
```
vim  /etc/supervisord.d/gunicorn.ini
```

- command： 即启动 gunicorn 的命令，此处要写 绝对路径
- directory： 项目部署目录，导入 startup.py 及其启动模块
```
[program:gunicorn]
command=/home/www/Genesis-Forum/back-end/venv3/bin/gunicorn startup:app -c deploy/gunicorn.conf.py
directory=/home/www/Genesis-Forum/back-end
user=root
autostart=true
autorestart=true
redirect_stderr=true
```

- 有了配置文件，就可以通过 Supervisor 来管理 Gunicorn 了
- 同理，我们在用 RQ 实现后台任务时，还需要启动 rq worker，所以这里也提供对应的 Supervisor 配置文件
```
vim  /etc/supervisord.d/rq-worker.ini
```

```
[program:rq-worker]
command=/home/www/back-end/venv3/bin/rq worker flask-tasks
numprocs=1
directory=/home/www/back-end
user=root
autostart=true
autorestart=true
redirect_stderr=true
```

- 增加配置文件后，需要更新，然后启动
```
supervisorctl reread

supervisorctl update
```

- 使用`ps -ef | grep gunicorn`，会发现 Gunicorn 进程已经被 Supervisor 启动起来了
- 启动/停止/重启 指令 (可选)
```
supervisorctl start gunicorn

supervisorctl stop gunicorn

supervisorctl restart gunicorn
```

## Nginx Install
***Nginx 是一个高性能的 HTTP 和反向代理服务器，专为性能优化而设计，能够处理大量并发连接，因此在动态和静态内容的快速交付方面表现出色。我们用来作为静态内容的 web 服务器、前端缓存和安全层，用它来反向代理vuejs应用***

- 添加repo源
```
vim /etc/yum.repos.d/nginx.repo
```

- CentOS 7 系统：
```
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/7/$basearch/
gpgcheck=0
enabled=1
```

- RedHat 9 系统：
```
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/mainline/rhel/9/$basearch/
gpgcheck=0
enabled=1
```

- 启动
```
yum install -y nginx

systemctl start nginx

systemctl enable nginx
```

- `npm run build`将新生成的 front-end/dist/ 目录下 所有文件 上传到服务器的 /usr/share/nginx/html/ 目录下
- html文件夹下应只有50x.html index.html static
- 访问http://x.x.x.x
```
cd /home/www/Genesis-Forum/front-end/dist

cp -r index.html static /usr/share/nginx/html/
```

<br><br>

# SSL证书配置

## Apply for an SSL Certificate
- cloudflare可以免费申请SSL证书到15年
- 下载证书的公钥pem和密钥key，这些是域名专属的
- 上传到Nginx服务器

## Upload to Nginx Server
- 用nginx -t查看nginx配置文件的位置，我是/usr/local/nginx/conf/nginx.conf
- 创建证书目录，命名为cert
- 上传pem和key到该文件夹

```
cd /usr/local/nginx/conf  

mkdir cert  
```

- 修改配置
```
vim /usr/local/nginx/conf/nginx.conf
```

```
server {
     #HTTPS的默认访问端口443。
     #如果未在此处配置HTTPS的默认访问端口，可能会造成Nginx无法启动。
     listen 443 ssl;
     
     #填写证书绑定的域名
     server_name <yourdomain>;
 
     #填写证书文件绝对路径
     ssl_certificate cert/<cert-file-name>.pem;
     #填写证书私钥文件绝对路径
     ssl_certificate_key cert/<cert-file-name>.key;
 
     ssl_session_cache shared:SSL:1m;
     ssl_session_timeout 5m;
	 
     #自定义设置使用的TLS协议的类型以及加密套件（以下为配置示例，请您自行评估是否需要配置）
     #TLS协议版本越高，HTTPS通信的安全性越高，但是相较于低版本TLS协议，高版本TLS协议对浏览器的兼容性较差。
     ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
     ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3;

     #表示优先使用服务端加密套件。默认开启
     ssl_prefer_server_ciphers on;
 
 
    location / {
           root html;
           index index.html index.htm;
    }
}
```

- 设置HTTP请求自动跳转HTTPS
```
server {
     #HTTPS的默认访问端口443。
     #如果未在此处配置HTTPS的默认访问端口，可能会造成Nginx无法启动。
     listen 443 ssl;
     
     #填写证书绑定的域名
     server_name <yourdomain>;
 
     #填写证书文件绝对路径
     ssl_certificate cert/<cert-file-name>.pem;
     #填写证书私钥文件绝对路径
     ssl_certificate_key cert/<cert-file-name>.key;
 
     ssl_session_cache shared:SSL:1m;
     ssl_session_timeout 5m;
	 
     #自定义设置使用的TLS协议的类型以及加密套件（以下为配置示例，请您自行评估是否需要配置）
     #TLS协议版本越高，HTTPS通信的安全性越高，但是相较于低版本TLS协议，高版本TLS协议对浏览器的兼容性较差。
     ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
     ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3;

     #表示优先使用服务端加密套件。默认开启
     ssl_prefer_server_ciphers on;
 
 
    location / {
           root html;
           index index.html index.htm;
    }
}
server {
    listen 80;
    #填写证书绑定的域名
    server_name <yourdomain>;
    #将所有HTTP请求通过rewrite指令重定向到HTTPS。
    rewrite ^(.*)$ https://$host$1;
    location / {
        index index.html index.htm;
    }
}
```

## Upload to Gunicorn Server
- 修改 back-end/deploy/gunicorn.conf.py
```
import multiprocessing

bind = '0.0.0.0:5000'
workers = multiprocessing.cpu_count() * 2 + 1
# daemon = True
pidfile = '/run/gunicorn.pid'
loglevel = 'info'
errorlog = '/tmp/gunicorn-error.log'
accesslog = '/tmp/gunicorn-access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

certfile = '/path/to/your/certificate.crt'  # SSL证书文件路径
keyfile = '/path/to/your/private.key'  # SSL证书的私钥文件路径

```

<br><br>

# 防火墙配置与部署错误处理

## FireWall Configure and Chrome Error

- 接下来记得配置防火墙
- 具体详情点击[这里](firewall.md)

---