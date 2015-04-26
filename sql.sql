create table dubs(id bigserial primary key, url char(256),ol char(256) UNIQUE, votes int);
create table votes(id bigserial primary key, vid int);
