-- insert sample data into each table

insert into Users (username, favorite_genre)
values
    ('john_doe', 'Rock'),
    ('jane_smith', 'Pop'),
    ('alice_wonder', 'Jazz'),
    ('bob_marley', 'Reggae'),
    ('sarah_connor', 'Hip-Hop'),
    ('bruce_wayne', 'Classical'),
    ('clark_kent', 'Country'),
    ('tony_stark', 'Electronic'),
    ('diana_prince', 'R&B'),
    ('donald_trump', 'Rap');


insert into Artists (name, genre, debut_year)
values  
    ('The Beatles', 'Rock', 1960),
    ('Taylor Swift', 'Pop', 2006),
    ('Miles Davis', 'Jazz', 1944),
    ('Bob Marley', 'Reggae', 1963),
    ('Kanye West', 'Hip-Hop', 2004),
    ('Ludwig van Beethoven', 'Classical', 1787),
    ('Johnny Cash', 'Country', 1955),
    ('Daft Punk', 'Electronic', 1993),
    ('Beyoncé', 'R&B', 1997),
    ('Adele', 'Pop', 2008),
    ('Metallica', 'Metal', 1981);


insert into Songs (title, artist_id, genre, duration, release_year)
values
    ('Hey Jude', 1, 'Rock', 431, 1968),
    ('Shake It Off', 2, 'Pop', 242, 2014),
    ('So What', 3, 'Jazz', 545, 1959),
    ('Redemption Song', 4, 'Reggae', 227, 1980),
    ('Yesterday', 1, 'Rock', 125, 1965),
    ('All Too Well', 2, 'Pop', 321, 2012),
    ('Stronger', 5, 'Hip-Hop', 310, 2007),
    ('Fifth Symphony', 6, 'Classical', 1815, 1808),
    ('Hurt', 7, 'Country', 215, 2002),
    ('One More Time', 8, 'Electronic', 320, 2000),
    ('Halo', 9, 'R&B', 262, 2008),
    ('Rolling in the Deep', 10, 'Pop', 228, 2011),
    ('Enter Sandman', 11, 'Metal', 332, 1991),
    ('Here Comes the Sun', 1, 'Rock', 355, 1975);


insert into ListeningHistory (user_id, song_id, rating, last_listened)
values
    (1, 1, 5, '2024-09-29 12:34:56'),   
    (1, 5, 4, '2024-09-30 09:22:45'),   
    (2, 2, 5, '2024-09-30 10:15:00'),   
    (3, 3, 5, '2024-09-28 15:10:22'),   
    (4, 4, 5, '2024-09-27 17:05:33'),   
    (2, 6, 4, '2024-09-30 12:00:00'),   
    (5, 12, 4, '2024-09-30 14:45:33'),  
    (6, 13, 5, '2024-09-29 09:32:01'),  
    (7, 14, 5, '2024-09-28 11:17:49'),  
    (8, 10, 5, '2024-09-29 19:04:22'),  
    (9, 11, 5, '2024-09-30 08:10:00'), 
    (10, 8, 4, '2024-09-30 09:22:45'),  
    (3, 7, 5, '2024-09-29 12:30:50'),   
    (2, 9, 4, '2024-09-28 15:00:00'),   
    (1, 14, 5, '2024-09-27 20:15:12');  


insert into Recommendations (user_id, recommended_song_id, recommendation_date)
values  
    (1, 2, '2024-09-30 13:45:00'),  
    (2, 3, '2024-09-30 14:20:00'),  
    (3, 1, '2024-09-30 15:30:00'),  
    (4, 6, '2024-09-30 16:00:00'),  
    (5, 10, '2024-09-30 17:45:00'), 
    (6, 11, '2024-09-30 18:30:00'), 
    (7, 8, '2024-09-30 19:00:00'),  
    (8, 7, '2024-09-30 19:30:00'),  
    (9, 14, '2024-09-30 20:00:00'), 
    (10, 12, '2024-09-30 20:30:00');