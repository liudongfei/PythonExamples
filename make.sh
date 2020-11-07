#!/usr/bin/env bash

echo "开始制作镜像..."
image_tag=`date +%Y%m%d` #_%H%M
echo "当前时间：$image_tag"
docker build -t registry.cn-shanghai.aliyuncs.com/liudongfei/python:v${image_tag} .
echo "制作镜像成功!"

docker login --username=改变世界的琅琊 -p=liudf110628 registry.cn-shanghai.aliyuncs.com

# push镜像
docker push registry.cn-shanghai.aliyuncs.com/liudongfei/python:v${image_tag}

echo "镜像版本保存"
# 将最新的版本的镜像重命名为：latest,并push
docker tag registry.cn-shanghai.aliyuncs.com/liudongfei/python:v${image_tag} registry.cn-shanghai.aliyuncs.com/liudongfei/python:latest
docker push registry.cn-shanghai.aliyuncs.com/liudongfei/python:latest

echo "删除本地镜像"
docker rmi registry.cn-shanghai.aliyuncs.com/liudongfei/python:v${image_tag}

docker run -t --rm --name=hello registry.cn-shanghai.aliyuncs.com/liudongfei/python python -W ignore pandas_demo/pandas_test.py