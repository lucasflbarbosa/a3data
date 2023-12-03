FROM python:3.11-slim

LABEL Description="A3Data Technical Challenge"

ENV PYTHONIOENCODING utf-8

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc

RUN pip3 install --upgrade pip --no-cache-dir wheel

RUN cd /app && pip3 install --no-cache-dir -U -r requirements.txt

EXPOSE 8090

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8090"]