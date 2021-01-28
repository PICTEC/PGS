FROM node as builder
COPY . usr/src/app

ENV REACT_APP_SERVICE_PORT=80

WORKDIR usr/src/app

RUN yarn install
RUN yarn build
FROM nginx:latest
COPY --from=builder usr/src/app/build /usr/share/nginx/html
EXPOSE $REACT_APP_SERVICE_PORT

WORKDIR /usr/share/nginx/html
COPY ./getEnvAndRun.sh .
COPY .env .
RUN ["chmod", "+x", "getEnvAndRun.sh"]

CMD ["./getEnvAndRun.sh"]
