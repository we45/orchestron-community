FROM node:8
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD package.json /usr/src/app/package.json
RUN npm install && npm install -g serve
ADD . /usr/src/app
RUN npm run build
ENV PORT=80
CMD echo "{\"API_URL\": \"$API_URL\"}" > configure.json && serve -s dist
