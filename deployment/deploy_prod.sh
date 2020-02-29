#!/bin/sh

ssh root@103.108.140.130 <<EOF
  cd /var/www/html/jobsproject/jobsportal/
  git pull
  cd /var/www/html/jobsproject/
  source jobsenv/bin/activate
  cd jobsportal/
  cat requirements.txt | xargs -n 1 pip install
  python manage.py migrate
  sudo systemctl restart gunicorn
  exit
EOF
