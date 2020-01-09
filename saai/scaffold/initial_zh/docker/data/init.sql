create database bot;
use mysql;
select database();

create user dev@'%' identified by 'dev';
grant all on *.* to 'dev'@'%';

FLUSH PRIVILEGES;
