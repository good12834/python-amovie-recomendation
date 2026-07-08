import sqlite3
import json
import os


class Database:
    """SQLite database manager for persistent storage."""

    def __init__(self, db_path="moviebuddy.db"):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _get_connection(self):
        """Get a database connection."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def _init_db(self):
        """Initialize the database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                country TEXT DEFAULT '',
                language TEXT DEFAULT '',
                age TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                genre TEXT DEFAULT '',
                actor TEXT DEFAULT '',
                director TEXT DEFAULT '',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Movies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                genre TEXT NOT NULL,
                year INTEGER,
                rating REAL DEFAULT 0,
                director TEXT DEFAULT '',
                actors TEXT DEFAULT ''
            )
        """)

        # History table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie TEXT NOT NULL,
                watched_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Ratings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 10),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, movie)
            )
        """)

        # Favorites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, movie)
            )
        """)

        conn.commit()

    def import_movies_from_json(self, json_file="movies.json"):
        """Import movies from JSON file into the database."""
        if not os.path.exists(json_file):
            return

        with open(json_file, 'r', encoding='utf-8') as f:
            movies = json.load(f)

        conn = self._get_connection()
        cursor = conn.cursor()

        for movie in movies:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO movies (title, genre, year, rating, director, actors)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    movie["title"],
                    movie["genre"],
                    movie.get("year"),
                    movie.get("rating", 0),
                    movie.get("director", ""),
                    ", ".join(movie.get("actors", []))
                ))
            except sqlite3.Error:
                pass

        conn.commit()

    def get_or_create_user(self, name):
        """Get a user by name or create if not exists."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        user = cursor.fetchone()

        if user:
            return dict(user)

        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()

        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return dict(cursor.fetchone())

    def update_user(self, user_id, **kwargs):
        """Update user fields."""
        conn = self._get_connection()
        cursor = conn.cursor()

        allowed_fields = ["country", "language", "age"]
        for key, value in kwargs.items():
            if key in allowed_fields:
                cursor.execute(f"UPDATE users SET {key} = ? WHERE id = ?", (value, user_id))

        conn.commit()

    def add_preference(self, user_id, pref_type, value):
        """Add a user preference."""
        conn = self._get_connection()
        cursor = conn.cursor()

        if pref_type == "genre":
            cursor.execute("INSERT OR IGNORE INTO preferences (user_id, genre) VALUES (?, ?)",
                          (user_id, value))
        elif pref_type == "actor":
            cursor.execute("INSERT OR IGNORE INTO preferences (user_id, actor) VALUES (?, ?)",
                          (user_id, value))
        elif pref_type == "director":
            cursor.execute("INSERT OR IGNORE INTO preferences (user_id, director) VALUES (?, ?)",
                          (user_id, value))

        conn.commit()

    def get_preferences(self, user_id):
        """Get all preferences for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT genre, actor, director FROM preferences WHERE user_id = ?
        """, (user_id,))

        genres = set()
        actors = set()
        directors = set()

        for row in cursor.fetchall():
            if row["genre"]:
                genres.add(row["genre"])
            if row["actor"]:
                actors.add(row["actor"])
            if row["director"]:
                directors.add(row["director"])

        return {
            "genres": list(genres),
            "actors": list(actors),
            "directors": list(directors)
        }

    def add_to_history(self, user_id, movie):
        """Add a movie to user's watch history."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (user_id, movie) VALUES (?, ?)", (user_id, movie))
        conn.commit()

    def get_history(self, user_id):
        """Get watch history for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT movie, watched_date FROM history
            WHERE user_id = ? ORDER BY watched_date DESC
        """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]

    def add_rating(self, user_id, movie, rating):
        """Add or update a movie rating."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ratings (user_id, movie, rating)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, movie) DO UPDATE SET rating = ?
        """, (user_id, movie, rating, rating))
        conn.commit()

    def get_ratings(self, user_id):
        """Get all ratings for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT movie, rating FROM ratings WHERE user_id = ?", (user_id,))
        return {row["movie"]: row["rating"] for row in cursor.fetchall()}

    def add_favorite(self, user_id, movie):
        """Add a movie to user's favorites."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO favorites (user_id, movie) VALUES (?, ?)",
                      (user_id, movie))
        conn.commit()

    def get_favorites(self, user_id):
        """Get favorites for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT movie FROM favorites WHERE user_id = ?", (user_id,))
        return [row["movie"] for row in cursor.fetchall()]

    def clear_user_data(self, user_id):
        """Clear all data for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM preferences WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM history WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM ratings WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM favorites WHERE user_id = ?", (user_id,))
        cursor.execute("UPDATE users SET country = '', language = '', age = '' WHERE id = ?",
                      (user_id,))
        conn.commit()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None