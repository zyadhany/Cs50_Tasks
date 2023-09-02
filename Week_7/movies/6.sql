SELECT avg(rating) FROM ratings WHERE movie_id in (SELECT id FROM movies WHERE year is '2012');
