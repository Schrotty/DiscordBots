create table ignored_user
(
    id varchar(256) not null,
    constraint ignored_user_id_uindex
        unique (id)
);

