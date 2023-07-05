FROM node:lts-slim

WORKDIR /opt/app

COPY . .

RUN [ "npm", "install" ]

RUN [ "npm", "run", "build" ]

RUN [ "mkdir", "-p", "/opt/prod/build" ]

RUN [ "mv", "./build", "/opt/prod/build" ]

RUN [ "mv", "./package.json" ,"/opt/prod/build" ]

RUN [ "mv", "./package-lock.json", "/opt/prod/build" ]

WORKDIR /opt/prod/build

RUN [ "npm", "ci", "--omit", "dev" ]

ENTRYPOINT [ "node", "build" ]

