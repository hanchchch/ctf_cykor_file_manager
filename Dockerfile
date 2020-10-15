FROM ubuntu:18.04
RUN useradd -m -d /home/user -s /bin/bash -u 1000 user
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3-pip

COPY ./app /app

RUN pip3 install flask

EXPOSE 8080
WORKDIR /app
CMD ["/usr/bin/python3","app.py"]
