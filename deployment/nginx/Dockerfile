#FROM tutum/nginx
##FROM nginx:1.21-alpine
#
#RUN rm /etc/nginx/sites-enabled/default || true
#
#COPY sites-enabled/ /etc/nginx/sites-enabled

FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf || true
COPY nginx.conf /etc/nginx/conf.d
