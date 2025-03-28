import mysql.connector
import pandas as pd
import json

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='0000',
    database='movies_db'
)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT UNIQUE NOT NULL,
    title VARCHAR(255),
    release_date VARCHAR(20),
    overview TEXT,
    poster_path VARCHAR(255),
    budget BIGINT,
    revenue BIGINT,
    popularity FLOAT,
    vote_average FLOAT,
    vote_count INT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
)
''')

conn.commit()

# Load CSV data
data = pd.read_csv("10000 Movies Data.csv")

for _, row in data.iterrows():
    # Handle NaN values
    overview = row['overview'] if pd.notna(row['overview']) else ""

    # Insert movie
    cursor.execute('''
        INSERT INTO movies (movie_id, title, release_date, overview, poster_path, budget, revenue, popularity, vote_average, vote_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE title=VALUES(title)
    ''', (row['Movie_id'], row['title'], row['release_date'], overview, row['poster_path'], row['Budget'], row['Revenue'], row['popularity'], row['vote_average'], row['vote_count']))
    
    conn.commit()

    # Handle genres
    if isinstance(row['Genres'], str):
        try:
            genres = json.loads(row['Genres'])  # Convert JSON string to dictionary
            genre_names = [genre["name"] for genre in genres.values()]
        except:
            genre_names = []
        
        for genre in genre_names:
            cursor.execute("INSERT IGNORE INTO genres (name) VALUES (%s)", (genre,))
            cursor.execute("SELECT id FROM genres WHERE name = %s", (genre,))
            genre_id = cursor.fetchone()[0]
            cursor.execute("INSERT IGNORE INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (row['Movie_id'], genre_id))
    
    conn.commit()

conn.close()
