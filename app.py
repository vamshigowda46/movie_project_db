from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# 🔗 MySQL Connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="2007",  # change if needed
    database="movie_db"
)

# 🏠 HOME PAGE
@app.route('/')
def home():
    cursor = conn.cursor()

    cursor.execute("""
    SELECT users.name, movies.title, movies.genre, ratings.rating
    FROM ratings
    JOIN users ON users.user_id = ratings.user_id
    JOIN movies ON movies.movie_id = ratings.movie_id
    """)

    data = cursor.fetchall()

    return render_template("index.html", data=data)


# 🔍 SEARCH MOVIE
@app.route('/search', methods=['GET'])
def search():
    name = request.args.get('name')

    cursor = conn.cursor()

    query = """
    SELECT users.name, movies.title, movies.genre, ratings.rating
    FROM ratings
    JOIN users ON users.user_id = ratings.user_id
    JOIN movies ON movies.movie_id = ratings.movie_id
    WHERE movies.title LIKE %s
    """

    cursor.execute(query, ("%" + name + "%",))
    results = cursor.fetchall()

    return render_template("index.html", data=results)


# ⭐ TOP MOVIE
@app.route('/top')
def top():
    cursor = conn.cursor()

    query = """
    SELECT movies.title, ratings.rating
    FROM ratings
    JOIN movies ON movies.movie_id = ratings.movie_id
    ORDER BY ratings.rating DESC LIMIT 1
    """

    cursor.execute(query)
    top = cursor.fetchone()

    return render_template("top.html", top=top)


# ➕ ADD DATA
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user = request.form['user']
        movie = request.form['movie']
        genre = request.form['genre']
        rating = request.form['rating']

        cursor = conn.cursor()

        # insert user
        cursor.execute("INSERT INTO users (name) VALUES (%s)", (user,))
        user_id = cursor.lastrowid

        # insert movie
        cursor.execute("INSERT INTO movies (title, genre) VALUES (%s, %s)", (movie, genre))
        movie_id = cursor.lastrowid

        # insert rating
        cursor.execute(
            "INSERT INTO ratings (user_id, movie_id, rating) VALUES (%s, %s, %s)",
            (user_id, movie_id, rating)
        )

        conn.commit()

        return redirect('/')

    return render_template("add.html")


# ▶️ RUN
if __name__ == '__main__':
    app.run(debug=True)
