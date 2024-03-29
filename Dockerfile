FROM neo4j:4.2.7

WORKDIR /app

ADD requirement.txt .
ADD conf/credentials /root/.aws/credentials
ADD conf/neo4j.conf /var/lib/neo4j/conf/neo4j.conf

RUN apt update && \
  apt install -y  procps \
  vim \
  net-tools\
  python3 \
  python3-pip &&\
  pip3 install --upgrade pip &&\
  pip3 install -r requirement.txt

CMD neo4j start && cd html && python3 ../webserver.py 8000