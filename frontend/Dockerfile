FROM node:lts-slim

WORKDIR /opt/app

RUN [ "npm", "install", "http-server"]

COPY . .

RUN [ "npm", "install" ]

RUN [ "npm", "run", "build" ]

ENTRYPOINT [ "http-server", "dist" ]