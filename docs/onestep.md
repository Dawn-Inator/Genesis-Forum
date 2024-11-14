<br>

# Docker一键部署
- 获取权限
```
sudo -i
```

- 克隆仓库
```
yum install -y git

git clone https://github.com/Dawn-Inator/Genesis-Forum.git -b docker

cd Genesis-Forum
```

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
```
vim back-end/config.py
```

```
    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = 1
    MAIL_USERNAME='服务器的qq邮箱'
    MAIL_PASSWORD='qq邮箱的授权码'
    MAIL_SENDER='发送者的名字'
    ADMINS = ['admin_1@qq.com','admin_2@qq.com']  # 管理员的邮箱地址
```

- 修改cloudflare授权码

```
vim front-end/src/components/Auth/Login.vue
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

- 没有cloudflare授权码？？
```
vim front-end/src/components/Auth/Login.vue
```

```
<div class="text-center">
  <cfturnstile
    :sitekey="cf_sitekey"
    @verify="cf_callback"
  />
  <button type="submit" class="btn btn-primary" :disabled="!cf_token">{{ $t('auth.login.sign-in') }}</button>
</div>
```
- 把`:disabled="!cf_token"`删掉


- 启动！！
```
chmod +x onestep.sh&&./onestep.sh
```

- 以后启动和关闭项目用以下命令
```
docker-compose up -d

docker-compose stop
```

<br><br>

# 网站配置和SSL申请

## NPM and SSL Configure
***Nginx Proxy Manager(NPM)可以代理应用并管理域名和网站流量，也可以一步申请SSL证书，使用的是Let's encryt的证书*** 

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

nginx: 8080

flask-api: 5000

nginx-proxy-manager:81
```

<br><br>

# 防火墙配置与部署错误处理

## FireWall Configure and Chrome Error

- 接下来记得配置防火墙
- 具体详情点击[这里](firewall.md)

---
