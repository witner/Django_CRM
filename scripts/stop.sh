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
if [[ -f scripts/uwsgi.pid ]]
then
  `uwsgi --stop ./scripts/uwsgi.pid`
else
  PID=`/usr/sbin/lsof -i:5500|grep -v PID|awk '{print $2}'`
  if [[ "x${PID}" == "x" ]]
  then
    echo "没有找到运行的进程，不需要结束"
  else
    echo "当前进程PID：${PID},结束当前进程"
    kill -9 ${PID}
  fi
fi






