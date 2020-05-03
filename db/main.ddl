create table if not exists post (
    id serial primary key,
    post text not null,
    time timestamp not null
);
