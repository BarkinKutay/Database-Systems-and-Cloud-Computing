AIN3003 Barkın Kutay Özgünhan 2002044

# Q1: Find Movies From 70s

SELECT year, title FROM movies
WHERE(year BETWEEN 1970 AND 1979)
ORDER BY year;

# Q2: Find the number of movies of each director and order in descending order.

SELECT d.name, COUNT(md.movieID) AS total
FROM directors d, moviedirectors md
WHERE d.directorID = md.directorID
GROUP BY name
ORDER BY total DESC;

# Q3: Find the number of genres of each director's movies and order in descending order.

SELECT d.name, COUNT(DISTINCT g.description) AS total, GROUP_CONCAT(DISTINCT g.description) AS genres
FROM moviegenres mg, moviedirectors md, directors d, genres g
WHERE md.directorID = d.directorID
AND md.movieID = mg.movieID
AND g.genreID = mg.genreID
GROUP BY name
ORDER BY total desc;

# Q4: Find the list of movies having the genres "Drama" and "Comedy" only.

SELECT m.title, m.year, GROUP_CONCAT(g.description) AS genres
FROM moviegenres mg, movies m, genres g
WHERE mg.genreID IN (1,2)
AND m.movieID = mg.movieID
AND g.genreID = mg.genreID
GROUP BY title, year
HAVING COUNT(mg.genreID) = 2
ORDER BY year;

# Q5: Find and list the histogram of movies where bins are genres.

SELECT g.description genre, COUNT(mg.movieID) AS total
FROM genres g, moviegenres mg
WHERE g.genreID = mg.genreID
GROUP BY genre
ORDER BY total DESC;