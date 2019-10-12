#!/bin/bash -il
# 刷新环境变量
source ~/.bashrc
source ~/.bash_profile
source /etc/profile
# 项目名称
PROJECT_NAME=Django_CRM

# 项目主目录
BASE_DIR=/opt/deploy/

# 项目目录
PROJECT_DIR=${BASE_DIR}${PROJECT_NAME}
cd ${PROJECT_DIR}

# 启动python web容器uwsgi
`uwsgi --ini ./configs/uWSGI.ini`
# 重启nginx
`/usr/local/nginx/sbin/nginx -s reload`