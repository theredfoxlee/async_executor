FROM phusion/baseimage:0.11

RUN apt-get update

RUN apt-get install -y mpich
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

RUN pip3 install dramatiq[rabbitmq,watch]==1.6
RUN pip3 install flask==1.0
RUN pip3 install flask-restful==0.3
RUN pip3 install rom==0.42
RUN pip3 install rabbitmq==0.2

RUN mkdir -p /var/run/sshd

COPY ./keys/id_rsa /root/.ssh/id_rsa
COPY ./keys/id_rsa.pub /root/.ssh/authorized_keys

RUN echo "StrictHostKeyChecking no" > /root/.ssh/config

COPY ./apps/fate.c ./apps/fate.c
COPY ./apps/fermat.c ./apps/fermat.c

RUN mpicc -o ./fate ./apps/fate.c
RUN mpicc -o ./fermat ./apps/fermat.c

COPY ./async_executor/ ./async_executor

EXPOSE 5000

# turn on sshd
RUN rm -f /etc/service/sshd/down
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

ENTRYPOINT flask run
