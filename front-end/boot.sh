#!/bin/bash

# 复制静态文件
cp -r /app/dist/* /usr/share/nginx/html/

# 启动 Nginx
exec nginx -g 'daemon off;'
