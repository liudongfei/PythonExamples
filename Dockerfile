FROM python:3.7

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

#设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /usr/src/app
ENV PYTHONPATH=/usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

CMD python