from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='0000',
        database='movies_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/movies')
def get_movies():
    conn = get_db_connection()
    cursor = conn.cursor()

    limit = int(request.args.get("limit", 10))
    page = int(request.args.get("page", 1))
    offset = (page - 1) * limit

    cursor.execute(
        """
        SELECT m.movie_id, m.title, g.name AS genre 
        FROM movies m
        LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN genres g ON mg.genre_id = g.id
        LIMIT %s OFFSET %s
        """, (limit, offset)
    )

    movies = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"page": page, "limit": limit, "movies": movies})

@app.route('/movie-genres')
def get_movie_genres():
    conn = get_db_connection()
    cursor = conn.cursor()

    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    offset = (page - 1) * limit

    cursor.execute(
        """
        SELECT m.movie_id, m.title AS movie_title, g.id AS genre_id, g.name AS genre_name
        FROM movies m
        LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN genres g ON mg.genre_id = g.id
        ORDER BY m.movie_id
        LIMIT %s OFFSET %s
        """, (limit, offset)
    )

    movie_genres = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"page": page, "limit": limit, "movie_genres": movie_genres})

if __name__ == '__main__':
    app.run(debug=True)
