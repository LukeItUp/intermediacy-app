FROM python:3.6

RUN apt-get update && \
      apt-get -y install python3-dev

RUN mkdir /intermediacy-api

ADD . /intermediacy-api

WORKDIR /intermediacy-api

RUN pip3 install -r /intermediacy-api/requirements.txt

CMD python run.py