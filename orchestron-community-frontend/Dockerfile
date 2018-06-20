FROM node:8
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD package.json /usr/src/app/package.json
RUN npm install && npm install pm2 nodemon -g && npm install -g serve
ADD . /usr/src/app
RUN apt update && apt install -y vim
RUN npm run build
# RUN rm -rf ./build && rm -rf ./src
ENV PORT=80
CMD serve -s dist
