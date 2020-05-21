FROM python:3.8

RUN apt-get -q update && apt-get -y install netcat

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN cat ./config_for_docker.yaml > ./application/config.yaml

RUN cat ./application/config.yaml

RUN pip install -r requirements.txt

RUN curl -OL https://raw.githubusercontent.com/mrako/wait-for/master/wait-for && chmod +x wait-for

RUN python3 setup.py develop

RUN ./wait-for db:5432 -- start_app

RUN bash <(curl -s https://codecov.io/bash)