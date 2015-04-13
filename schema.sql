DROP TABLE if EXISTS users;
CREATE TABLE users (
  id integer primary key autoincrement,
  name text not null,
  added_on datetime not null default current_timestamp
);

DROP TABLE if EXISTS entries;
CREATE TABLE entries (
  id integer primary key autoincrement,
  word text not null,
  user integer not null,
  added_on datetime not null default current_timestamp,
  foreign key (user) references users (id)
);