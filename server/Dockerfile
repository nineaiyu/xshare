FROM python:3.9.14-slim

# Fixes some weird terminal issues such as broken clear / CTRL+L
ARG PIP_MIRROR=https://mirrors.aliyun.com/pypi/simple

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt update 

#RUN apt-get install g++ wget -y
#RUN apt-get install libssl-dev openssl libmariadb-dev  -y
RUN apt-get install libmariadb-dev  -y
RUN apt-get install g++  -y
RUN rm -rf /var/lib/apt/lists/* 



#COPY fir_client/dist /data/flyapps/fir_client

#RUN cd /opt/ && wget https://github.com/nineaiyu/zsign/archive/refs/tags/v1.1.2.tar.gz
# install pip
COPY requirements.txt /opt/requirements.txt
RUN cd /opt/ && pip install -U setuptools pip -i ${PIP_MIRROR} --ignore-installed && pip install --no-cache-dir -r requirements.txt -i ${PIP_MIRROR}  && pip install --no-cache-dir uwsgi -i ${PIP_MIRROR} 

#RUN rm -rf /var/cache/yum/

WORKDIR /data/server/
RUN addgroup --system --gid 101 nginx \
    && adduser --system --disabled-login --ingroup nginx --no-create-home --home /nonexistent --gecos "nginx user" --shell /bin/false --uid 101 nginx 


#ENTRYPOINT ["python", "manage.py", "start", "all","-u","nginx"]
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
