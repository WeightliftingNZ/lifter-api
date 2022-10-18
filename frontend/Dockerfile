FROM node:18

WORKDIR /code

COPY package*.json /code/

RUN npm install

COPY . /code/

RUN npm start

EXPOSE 3000
