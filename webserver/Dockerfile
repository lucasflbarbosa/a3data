FROM python:3.10-slim

LABEL Description="A3Data Technical Challenge"

ENV PYTHONIOENCODING utf-8

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc curl

RUN pip3 install --upgrade pip --no-cache-dir wheel

RUN cd /app && pip3 install --no-cache-dir -U -r requirements.txt

EXPOSE 8090

CMD ["/bin/sh", "-c", "while ! curl -s elasticsearch:9200; do sleep 1; done && python main.py"]