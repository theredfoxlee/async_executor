FROM ubuntu:19.10

RUN apt-get update

RUN apt-get install -y mpich
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y openssh-server

RUN pip3 install dramatiq[rabbitmq,watch]==1.6
RUN pip3 install flask==1.0
RUN pip3 install flask-restful==0.3
RUN pip3 install rom==0.42
# downgrade redis
RUN pip3 install -U redis==2.10.6
RUN pip3 install rabbitmq==0.2

COPY ./keys/id_rsa /root/.ssh/id_rsa
COPY ./keys/id_rsa.pub /root/.ssh/authorized_keys

RUN mkdir -p /var/run/sshd
RUN echo "StrictHostKeyChecking no" > /root/.ssh/config
RUN sed -i \
  's#PermitRootLogin prohibit-password#PermitRootLogin yes#' \
  /etc/ssh/sshd_config
RUN sed -i \
  's#session\s*required\s*pam_loginuid.so#session optional pam_loginuid.so#g' \
  /etc/pam.d/sshd

COPY ./apps/fate.c ./apps/fate.c
COPY ./apps/fermat.c ./apps/fermat.c

RUN mpicc -o ./fate ./apps/fate.c
RUN mpicc -o ./fermat ./apps/fermat.c

COPY ./async_executor/ ./async_executor

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8 

ENV FLASK_APP=async_executor.main

EXPOSE 5000
EXPOSE 22

#ENTRYPOINT /usr/sbin/sshd && flask run --host 0.0.0.0

