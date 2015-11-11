create table dubs(id BIGINT primary key AUTO_INCREMENT, url varchar(256),ol varchar(256) UNIQUE, votes int);
create table votes(id BIGINT primary key AUTO_INCREMENT, vid int);
create table dubvideos(id BIGINT primary key AUTO_INCREMENT, url varchar(256),ol varchar(256) UNIQUE, lang int);
