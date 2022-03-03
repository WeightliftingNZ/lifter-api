FROM node:17-alpine

WORKDIR /code

COPY yarn.lock package.json /code/
RUN yarn install

COPY . /code/
