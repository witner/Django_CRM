#!/bin/bash -il
# 刷新环境变量
source ~/.bashrc
# 项目名称
PROJECT_NAME=Django_CRM

# 项目主目录
BASE_DIR=/opt/deploy/

# 项目目录
PROJECT_DIR=${BASE_DIR}${PROJECT_NAME}

# 安装包名称
PROJECT_PAGKAGE_NAME=${PROJECT_NAME}'.tgz'

# 打包
tar -zcf ${PROJECT_PAGKAGE_NAME} ./*

# 判断程序目录是否存在
if [[ ! -d ${BASE_DIR} ]]
then
  mkdir -p ${BASE_DIR}
fi

# 判断项目目录是否存在
if [[ ! -d ${PROJECT_DIR} ]]
then
    mkdir -p ${PROJECT_DIR}
else
    # 删除原目录下的代码
    rm -rf ${PROJECT_DIR}/*
fi

# 自动创建日志日志，防止目录不存在时报错
if [ ! -d ${PROJECT_DIR}/"logs" ]
then
    mkdir -p ${PROJECT_DIR}/logs
fi


# 分发新包
mv ${PROJECT_PAGKAGE_NAME} ${PROJECT_DIR}

# 进行项目主目录，解压新安装包
cd ${PROJECT_DIR} && tar -zxf ${PROJECT_PAGKAGE_NAME} && rm -f ${PROJECT_PAGKAGE_NAME}

## 根据Pipfile创建python虚拟环境
#`pipenv install`
##
#`pipenv --venv`

# 将对于Nginx配置移动到对应目录
cp ./configs/nginx.conf /usr/local/nginx/conf.d/${PROJECT_NAME}.conf
