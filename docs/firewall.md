<br>

# 目录导航

## 网络与防火墙配置

### [FireWall configure](#firewall-configure-1)

### [Console Error](#console-error-1)

### [pip Download Error](#pip-download-error-1)

### [Azure Root Login](#azure-root-login-1)

## 浏览器与部署错误处理

### [CORS Policy Blocking](#cors-policy-blocking-1)

### [Cookie-Token Error](#cookie-token-error-1)

### [Redirect Error](#redirect-error-1)

### [Cannot Connect Back-End Server](#cannot-connect-back-end-server-1)

<br><br>

# 网络与防火墙配置

## FireWall configure
- 开启端口
- (以下必开)
- npm登录端口为81
- http端口是80
- https端口是443
- 邮箱出站的目标端口是465(在第三方防火墙设置)
- ···
- (以下可选)
- 5000是后端端口
- 8080是前端端口
- 这些都用npm代理域名，可以关闭
```
firewall-cmd --zone=public --permanent --add-service=http

firewall-cmd --zone=public --permanent --add-service=https

firewall-cmd --zone=public --permanent --add-port=81/tcp

firewall-cmd --zone=public --permanent --add-port=5000/tcp

firewall-cmd --zone=public --permanent --add-port=8080/tcp

firewall-cmd --reload

ss -tulnp
```

- 暂时关闭防火墙（重启后防火墙会自动启动）
- 永久关闭防火墙（需要手动重新启动）
```
systemctl stop firewalld

systemctl disable firewalld
```

## Console Error
- `Error: Connection closed by foreign host. `
- *Solve: close or change your proxy and retry the network connecting.*

## pip Download Error
- pip的下载速度很慢，可以将 安装源为国内的源（比如 aliyun）
```
mkdir ~/.pip

vim ~/.pip/pip.conf
```

```
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```

## Azure Root Login
- 进入root，创建.ssh文件夹
- 将root账号也设置为密钥登录
```
sudo -i

mkdir /root/.ssh/

cp /home/azureuser/.ssh/authorized_keys /root/.ssh/
```

- 同理可用于AWS

<br><br>

# 浏览器与部署错误处理

## CORS Policy Blocking
- Access to XMLHttpRequest at 'http://x.x.x.x:5000/api/tokens' from origin 'http://x.x.x.x:8080' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```
原因是

1 前端直接使用npm run start部署，没有web代理器，并不安全。所以被chrome浏览器拒绝访问

-> 使用Nginx代理vuejs应用，实现安全协议

2 Gunicorn代理了flask应用，但是flask并没有正常的启动

-> 调试后端，ping一下

3 Nginx安装了ssl证书，但是gunicorn并没有安装

-> gunicorn也安装ssl证书

4 前端应用和后端服务位于不同的域名下，导致浏览器报错。如www.forum.com和www.forum.org

-> 应该保证前端后端都是用*.forum.com的网址
```

- 更多CORS错误原理请参考[这里](https://blog.huli.tw/2021/02/19/cors-guide-1/)

## Cookie-Token Error
- Uncaught TypeError: JSON.parse(...).permissions.split is not a function
```
原因是后端更新后导致前端的Cookie对接错误

-> 清除浏览器网站数据或者更换浏览器
```

## Redirect Error
- redirect error,page not work
```
浏览器重定向次数过多，清除浏览器网站数据或者更换浏览器即可
```

## Cannot Connect Back-End Server
- http://127.0.0.1:5000/ network error
- http://x.x.x.x:5000/api/ping close ping
```
注意后端需要以 -h 0.0.0.0 启动才能被外部ip访问，-h 127.0.0.1 只能被本机ip访问
记得打开5000端口
外部访问时前端需要连接 http://x.x.x.x:5000 才行，连接127.0.0.1无效
```

## Too Much Times to Redirect
- 网页重定向过多，网页打不开
```
-> 在 CloudFlare 的 SSL/TLS 菜单里将「SSL/TLS 加密模式」设置为完全（Strict）即可。

-> https://blog.csdn.net/hkjsa/article/details/131197831
```
---