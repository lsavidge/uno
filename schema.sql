DROP TABLE if EXISTS entries;
CREATE TABLE entries (
  id integer primary key autoincrement,
  word text not null,
  added_on datetime not null default current_timestamp
);