SELECT name FROM people
JOIN directors ON people.id = person_id
JOIN ratings ON ratings.movie_id = directors.movie_id
WHERE rating >= 9.0;