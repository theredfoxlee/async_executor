FROM ubuntu:19.10

RUN apt-get update

RUN apt-get install -y mpich
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

RUN apt-get install -y openssh-server
RUN apt-get install -y supervisor

RUN pip3 install dramatiq[rabbitmq,watch]==1.6
RUN pip3 install flask==1.0
RUN pip3 install flask-restful==0.3
RUN pip3 install rom==0.42
RUN pip3 install rabbitmq==0.2

RUN mkdir -p /var/run/sshd /etc/supervisor/conf.d

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY ./keys/id_rsa /root/.ssh/id_rsa
COPY ./keys/id_rsa.pub /root/.ssh/authorized_keys

RUN sed -i 's#PermitRootLogin prohibit-password#PermitRootLogin yes#' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

RUN echo "StrictHostKeyChecking no" > /root/.ssh/config

COPY ./apps/fate.c ./apps/fate.c
COPY ./apps/fermat.c ./apps/fermat.c
RUN mpicc -o ./fate ./apps/fate.c
RUN mpicc -o ./fermat ./apps/fermat.c

COPY ./async_executor/ ./async_executor

EXPOSE 22
EXPOSE 5000

#CMD ["/usr/bin/supervisord"]

ENTRYPOINT service ssh restart && service ssh status && flask run

