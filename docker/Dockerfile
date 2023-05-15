FROM python:3.10.6-alpine

WORKDIR app

RUN apk update && apk add supervisor

COPY server/ server/
COPY supervisord.conf /etc/supervisord.conf

RUN cd server/ && pip3 install -r requirements.txt

EXPOSE 2121
EXPOSE 9001

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
