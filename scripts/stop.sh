#!/bin/bash -il

# 刷新环境变量
source ~/.bashrc

# 项目名称
PROJECT_NAME=Django_CRM

# 项目主目录
BASE_DIR=/opt/deploy/

# 项目目录
PROJECT_DIR=${BASE_DIR}${PROJECT_NAME}
cd ${PROJECT_DIR}

# 停止python web容器uwsgi
`uwsgi --stop ./scripts/uwsgi.pid`