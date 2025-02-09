# Use the official Python image
FROM python:3.12
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y sqlite3 libsqlite3-dev && \
    apt-get install -y python3-pip
RUN mkdir /db /home/api
WORKDIR /home/api
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 3000