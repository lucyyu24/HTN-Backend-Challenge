drop table if exists user;
drop table if exists skill;

create table user (
    email        text primary key,
    name 		text,
    company		text,
    phone    	text,
    latitude	real,
    longitude	real,
    picture 	text
);

create table skill (
	name	text,
	rating  integer,
    userEmail   text
);