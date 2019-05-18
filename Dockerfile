FROM python:3.7.3-alpine

RUN apk add 'gcc=8.3.0-r0'
RUN apk add 'libc-dev=0.7.1-r0'

RUN apk add 'libffi-dev'
RUN apk add 'openssl-dev'
RUN apk add 'python3-dev'

RUN pip3 install --no-cache-dir "dramatiq[rabbitmq, watch]"
RUN pip3 install --no-cache-dir "flask==1.0.2"
RUN pip3 install --no-cache-dir "flask-restful==0.3.7"
RUN pip3 install --no-cache-dir "rom==0.42.5"
RUN pip3 install --no-cache-dir "redis==3.2.1"
RUN pip3 install --no-cache-dir "rabbitmq==0.2.0"

COPY async_executor async_executor

EXPOSE 5000
