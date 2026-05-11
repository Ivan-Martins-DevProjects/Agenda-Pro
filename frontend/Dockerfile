FROM nginx:alpine
WORKDIR /app

RUN rm -rf /usr/share/nginx/html/*

COPY . /usr/share/nginx/html/

EXPOSE 80

CMD ["/bin/sh", "-c", "sed -i 's|__API_URL_PLACEHOLDER__|'${API_URL}'|g' /usr/share/nginx/html/index.html && sed -i 's|__LOGIN_URL_PLACEHOLDER__|'${LOGIN_URL}'|g' /usr/share/nginx/html/login.html && nginx -g 'daemon off;'"]
