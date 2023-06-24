FROM python:3.10.6-alpine

ARG BUILD_DATE

# Metadata
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL maintainer="abduaziz.ziyodov@mail.ru"
LABEL description="Server image, for docker dashboard app"
LABEL url="https://github.com/AbduazizZiyodov/docker-dashboard"

WORKDIR /app

# Install dependencies
RUN apk update && apk add supervisor

# Copy server files
COPY server/ server/
COPY supervisord.conf /etc/supervisord.conf

# Install python packages
RUN cd server/ && pip3 install -r requirements.txt

# API port
EXPOSE 2121
# Supervisor inet HTTP port
EXPOSE 9001

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
