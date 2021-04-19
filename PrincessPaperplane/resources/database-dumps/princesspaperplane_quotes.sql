create table princesspaperplane.quotes
(
    id     int auto_increment,
    quote  text not null,
    author text not null,
    constraint quotes_id_uindex
        unique (id)
);