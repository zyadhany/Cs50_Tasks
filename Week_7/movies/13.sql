SELECT distinct(name) FROM people
JOIN stars ON people.id = person_id
JOIN movies ON movie_id = movies.id
WHERE name != 'Kevin Bacon' AND title IN
(
SELECT distinct(title) FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = person_id
WHERE name is 'Kevin Bacon' AND people.birth is '1958'
);