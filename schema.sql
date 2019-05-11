create table users
(
    id       integer primary key autoincrement,
    username varchar(32) unique,
    password char(64)
);

create table translations
(
    id         integer primary key autoincrement,
    user_id    integer,
    source     text,
    target     text,
    created_at datetime,
    foreign key (user_id) references users (id)
);