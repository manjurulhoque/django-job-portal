#!/bin/sh

ssh root@103.108.140.130 <<EOF
  cd /var/www/html/jobsproject/jobsportal/
  git pull
  cd /var/www/html/jobsproject/
  source jobsenv/bin/activate
  pip install -r requirements.txt
  ./manage.py migrate
  sudo systemctl restart jobsportal
  exit
EOF
