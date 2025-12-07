FROM nginx:alpine
WORKDIR /app

RUN rm -rf /usr/share/nginx/html/*

COPY ./app/ /usr/share/nginx/html/

EXPOSE 7000

CMD ["nginx", "-g", "daemon off;"]
