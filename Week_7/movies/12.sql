SELECT title FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = person_id
WHERE name is 'Bradley Cooper'AND title IN
(
SELECT title FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = person_id
WHERE name is 'Jennifer Lawrence'
);