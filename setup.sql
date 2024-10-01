-- CREATE TABLES for song rec database system: Users, Songs, Artists, ListeningHistory, Recommendations

create table Users (
    user_id serial primary key,
    username varchar(100) not null,
    favorite_genre varchar(50)
);

create table Artists (
    artist_id serial primary key,
    name varchar(100) not null,
    genre varchar(50),
    debut_year int
);

create table Songs (
    song_id serial primary key,
    title varchar(100) not null,
    artist_id int not null,
    genre varchar(50),
    duration int,
    release_year int,
    foreign key (artist_id) 
        references Artists(artist_id)
        on delete cascade
);

create table ListeningHistory (
    history_id serial primary key,
    user_id int references Users(user_id) on delete cascade,
    song_id int references Songs(song_id) on delete cascade,
    rating int check (rating between 1 and 5),
    last_listened timestamp default CURRENT_TIMESTAMP  
);

create table Recommendations (
    recommendation_id serial primary key,
    user_id int references Users(user_id) on delete cascade,
    recommended_song_id int references Songs(song_id) on delete cascade,
    recommendation_date timestamp default CURRENT_TIMESTAMP
);
