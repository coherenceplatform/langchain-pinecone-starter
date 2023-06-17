FROM node:16

COPY package.json package.json
COPY yarn.lock yarn.lock

RUN yarn install

COPY . .
