from mysql import connector
import sys

def linebreak(char="-",lenght=37):
    for x in range(round((lenght-1)/len(char))):
        print(char, end ="")
    print(char)
    
if __name__ == "__main__":
        
    my_connection = connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="imdb"
        )

    my_cursor = my_connection.cursor() 
    
    # region TASK 1
    linebreak("=")    
    print("TASK 1:")
    linebreak("- ") 
    
    # Find the movies from 70s. 

    my_cursor.execute(""" 
        SELECT year, title FROM movies
        WHERE(year BETWEEN 1970 AND 1979)
        ORDER BY year
    """) 
    print("{:40} {:4}".format("Movie Title", "Year")) 
    for row in my_cursor:   # type: ignore
        print(f"{row[1]:40} {row[0]:<4}")
    
    input("press enter to continue")
    #endregion
    
    # region TASK 2
    linebreak("=")    
    print("TASK 2:")
    linebreak("- ") 
    

    # Find the number of movies of each director. 

    my_cursor.execute(""" 
        SELECT d.name, COUNT(md.movieID) AS total
        FROM directors d, moviedirectors md
        WHERE d.directorID = md.directorID
        GROUP BY name
        ORDER BY total DESC
    """) 
    
    print("{:24} {:16}".format("Director Name", "Number of movies")) 
    
    for row in my_cursor: 
        print(f"{row[0]:24} {row[1]:<16}")
    
    input("press enter to continue")
    #endregion
    
    # region TASK 3
    linebreak("=")    
    print("TASK 3:")
    linebreak("- ") 

    # Find the number of genres of each director's movies. 

    my_cursor.execute(""" 
        SELECT d.name, COUNT(DISTINCT g.description) AS total, GROUP_CONCAT(DISTINCT g.description) AS genres
        FROM moviegenres mg, moviedirectors md, directors d, genres g
        WHERE md.directorID = d.directorID
        AND md.movieID = mg.movieID
        AND g.genreID = mg.genreID
        GROUP BY name
        ORDER BY total desc
    """) 
    
    print("{:24} {:16} {:100}".format("Director Name",  
                                    "Number of movies", "Genres")) 
    for row in my_cursor: 
        print(f"{row[0]:24} {row[1]:<16} {row[2]:<100}")
       
    input("press enter to continue") 
    #endregion
    
    # region TASK 4
    linebreak("=")    
    print("TASK 4:")
    linebreak("- ") 
    
    # Find the list of movies having the genres "Drama" and "Comedy" only. 

    my_cursor.execute(""" 
    SELECT m.title, m.year, GROUP_CONCAT(g.description) AS genres
    FROM moviegenres mg, movies m, genres g
    WHERE mg.genreID IN (1,2)
    AND m.movieID = mg.movieID
    AND g.genreID = mg.genreID
    GROUP BY title, year
    HAVING COUNT(mg.genreID) = 2
    ORDER BY year
    """) 
    
    print("{:32} {:4} {:100}".format("Movie Title", "Year", "Genres")) 
    for row in my_cursor: 
        print(f"{row[0]:32} {row[1]:4} {row[2]:<100}")
    
    input("press enter to continue")
    #endregion
    
    # region TASK 5
    linebreak("=")    
    print("TASK 5:")
    linebreak("- ") 
    
    # Find and list the histogram of movies where bins are genres. 

    my_cursor.execute(""" 
        SELECT g.description genre, COUNT(mg.movieID) AS total
        FROM genres g, moviegenres mg
        WHERE g.genreID = mg.genreID
        GROUP BY genre
        ORDER BY total DESC
    """) 
    
    print("{:32} {:4}".format("Genre", "Count")) 
    for row in my_cursor: 
        print(f"{row[0]:32} {row[1]:<4}")
#endregion