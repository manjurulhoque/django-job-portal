#!/bin/sh

ssh root@159.69.172.93 <<EOF
  cd projects/django/job-portal/
  git pull
  docker-compose -f docker-compose.prod.yml up --build -d
  exit
EOF