#!/bin/bash
# 项目名称
PROJECT_NAME=Django_CRM

# 项目主目录
BASE_DIR=/opt/deploy/

# 项目目录
PROJECT_DIR=${BASE_DIR}${PROJECT_NAME}
cd ${PROJECT_DIR}

# 启动python web容器uwsgi
`/usr/local/bin/uwsgi --ini ./configs/uWSGI.ini`
# 重启nginx
`/usr/local/nginx/sbin/nginx -s reload`