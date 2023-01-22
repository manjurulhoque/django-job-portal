FROM nginx:1.21-alpine

RUN rm /etc/nginx/sites-enabled/default || true

COPY sites-enabled/ /etc/nginx/sites-enabled
