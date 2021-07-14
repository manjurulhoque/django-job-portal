create database if not exists jobdb;
GRANT ALL PRIVILEGES ON `jobdb`.* To 'jobs_user'@'%';
FLUSH PRIVILEGES;
