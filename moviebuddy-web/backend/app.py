import os
import sqlite3
import json
import secrets
from datetime import datetime
from flask import Flask, request, jsonify, session, g
from flask_cors import CORS
from dotenv import load_dotenv
from tmdb_api import TMDBAPI
import ai_chat

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://localhost:5173"])
tmdb = TMDBAPI()

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moviebuddy.db")


def get_db():
    """Get database connection for current request."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db


def close_db(e=None):
    """Close database connection."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize database schema."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pref_type TEXT NOT NULL,
            pref_value TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, pref_type, pref_value)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_title TEXT NOT NULL,
            movie_id INTEGER,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 10),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, movie_title)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_title TEXT NOT NULL,
            movie_id INTEGER,
            poster TEXT DEFAULT '',
            year INTEGER,
            rating REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, movie_title)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watch_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_title TEXT NOT NULL,
            movie_id INTEGER,
            watched_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()


app.teardown_appcontext(close_db)


# ============================================================
# AUTH / USER ENDPOINTS
# ============================================================

@app.route("/api/auth/login", methods=["POST"])
def login():
    """Login or create a new user."""
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    name = data["name"].strip()
    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()

    if user is None:
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        db.commit()
        user_id = cursor.lastrowid
    else:
        user_id = user["id"]

    # Store user_id in session
    session["user_id"] = user_id
    session["user_name"] = name

    return jsonify({
        "success": True,
        "user": {
            "id": user_id,
            "name": name
        }
    })


@app.route("/api/auth/me", methods=["GET"])
def get_current_user():
    """Get current logged-in user info."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"user": None})

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        return jsonify({"user": None})

    return jsonify({
        "user": {
            "id": user["id"],
            "name": user["name"],
            "country": user["country"],
            "language": user["language"],
            "age": user["age"],
            "created_at": user["created_at"]
        }
    })


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    """Logout current user."""
    session.clear()
    return jsonify({"success": True})


# ============================================================
# MOVIE ENDPOINTS
# ============================================================

@app.route("/api/movies/popular", methods=["GET"])
def get_popular_movies():
    """Get popular movies."""
    page = request.args.get("page", 1, type=int)
    movies = tmdb.get_popular(page)
    return jsonify({"movies": movies})


@app.route("/api/movies/top-rated", methods=["GET"])
def get_top_rated_movies():
    """Get top rated movies."""
    page = request.args.get("page", 1, type=int)
    movies = tmdb.get_top_rated(page)
    return jsonify({"movies": movies})


@app.route("/api/movies/search", methods=["GET"])
def search_movies():
    """Search movies by title."""
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"movies": [], "error": "Query is required"}), 400
    page = request.args.get("page", 1, type=int)
    movies = tmdb.search_movies(query, page)
    return jsonify({"movies": movies})


@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def get_movie_details(movie_id):
    """Get details for a specific movie."""
    movie = tmdb.get_movie_details(movie_id)
    if movie is None:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify({"movie": movie})


@app.route("/api/movies/genre/<genre>", methods=["GET"])
def get_movies_by_genre(genre):
    """Get movies by genre."""
    page = request.args.get("page", 1, type=int)
    genres = [genre]
    movies = tmdb.get_by_genre(genres, page)
    return jsonify({"movies": movies})


@app.route("/api/genres", methods=["GET"])
def get_genres():
    """Get list of all genres."""
    genres = tmdb.get_genres_list()
    return jsonify({"genres": genres})


@app.route("/api/movies/<int:movie_id>/videos", methods=["GET"])
def get_movie_videos(movie_id):
    """Get videos (trailers) for a specific movie."""
    videos = tmdb.get_movie_videos(movie_id)
    return jsonify({"videos": videos})


@app.route("/api/movies/recommendations/<int:movie_id>", methods=["GET"])
def get_movie_recommendations(movie_id):
    """Get recommendations based on a movie."""
    movies = tmdb.get_recommendations(movie_id)
    return jsonify({"movies": movies})


# ============================================================
# USER PREFERENCES & MEMORY
# ============================================================

@app.route("/api/user/preferences", methods=["GET"])
def get_user_preferences():
    """Get user preferences."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT pref_type, pref_value FROM preferences WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()

    prefs = {"genres": [], "actors": [], "directors": [], "disliked_genres": []}
    for row in rows:
        ptype = row["pref_type"]
        pval = row["pref_value"]
        if ptype in prefs:
            prefs[ptype].append(pval)

    # Get user info
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        prefs["country"] = user["country"]
        prefs["language"] = user["language"]
        prefs["age"] = user["age"]

    # Get favorites
    cursor.execute("SELECT movie_title, movie_id, poster, year, rating FROM favorites WHERE user_id = ?", (user_id,))
    prefs["favorites"] = [dict(row) for row in cursor.fetchall()]

    # Get watch history
    cursor.execute("SELECT movie_title, movie_id, watched_date FROM watch_history WHERE user_id = ? ORDER BY watched_date DESC", (user_id,))
    prefs["watch_history"] = [dict(row) for row in cursor.fetchall()]

    # Get ratings
    cursor.execute("SELECT movie_title, rating FROM ratings WHERE user_id = ?", (user_id,))
    prefs["ratings"] = {row["movie_title"]: row["rating"] for row in cursor.fetchall()}

    return jsonify(prefs)


@app.route("/api/user/preferences", methods=["POST"])
def update_preferences():
    """Update user preferences."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    db = get_db()
    cursor = db.cursor()

    for key, value in data.items():
        if key in ["genres", "actors", "directors", "disliked_genres"]:
            if isinstance(value, str):
                values_list = [value]
            elif isinstance(value, list):
                values_list = value
            else:
                continue

            for v in values_list:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO preferences (user_id, pref_type, pref_value)
                        VALUES (?, ?, ?)
                    """, (user_id, key, v))
                except sqlite3.Error:
                    pass

        elif key in ["country", "language", "age"]:
            cursor.execute(f"UPDATE users SET {key} = ? WHERE id = ?", (value, user_id))

    db.commit()
    return jsonify({"success": True})


# ============================================================
# FAVORITES / RATINGS / HISTORY
# ============================================================

@app.route("/api/user/favorites", methods=["POST"])
def add_favorite():
    """Add a movie to favorites."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    if not data or "movie_title" not in data:
        return jsonify({"error": "movie_title is required"}), 400

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT OR IGNORE INTO favorites (user_id, movie_title, movie_id, poster, year, rating)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            data["movie_title"],
            data.get("movie_id"),
            data.get("poster", ""),
            data.get("year"),
            data.get("rating", 0)
        ))
        db.commit()
        return jsonify({"success": True})
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/user/favorites", methods=["DELETE"])
def remove_favorite():
    """Remove a movie from favorites."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    if not data or "movie_title" not in data:
        return jsonify({"error": "movie_title is required"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM favorites WHERE user_id = ? AND movie_title = ?",
                   (user_id, data["movie_title"]))
    db.commit()
    return jsonify({"success": True})


@app.route("/api/user/ratings", methods=["POST"])
def add_rating():
    """Rate a movie."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    if not data or "movie_title" not in data or "rating" not in data:
        return jsonify({"error": "movie_title and rating are required"}), 400

    rating = int(data["rating"])
    if rating < 1 or rating > 10:
        return jsonify({"error": "Rating must be between 1 and 10"}), 400

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO ratings (user_id, movie_title, movie_id, rating)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, movie_title) DO UPDATE SET rating = ?
        """, (user_id, data["movie_title"], data.get("movie_id"), rating, rating))
        db.commit()
        return jsonify({"success": True})
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/user/watch-history", methods=["POST"])
def add_to_watch_history():
    """Add a movie to watch history."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    if not data or "movie_title" not in data:
        return jsonify({"error": "movie_title is required"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO watch_history (user_id, movie_title, movie_id)
        VALUES (?, ?, ?)
    """, (user_id, data["movie_title"], data.get("movie_id")))
    db.commit()
    return jsonify({"success": True})


# ============================================================
# CHATBOT ENDPOINT
# ============================================================

class MovieChatBot:
    """Simple rule-based chatbot for movie recommendations."""

    def __init__(self):
        self.genre_keywords = {
            "action": "Action", "sci-fi": "Sci-Fi", "scifi": "Sci-Fi",
            "comedy": "Comedy", "drama": "Drama", "horror": "Horror",
            "thriller": "Thriller", "romance": "Romance", "crime": "Crime",
            "animation": "Animation", "anime": "Anime", "superhero": "Superhero",
            "marvel": "Superhero", "dc": "Superhero", "fantasy": "Fantasy",
            "mystery": "Mystery", "documentary": "Documentary", "war": "War",
            "musical": "Musical", "western": "Western"
        }
        self.mood_map = {
            "happy": "Comedy", "funny": "Comedy",
            "sad": "Drama", "emotional": "Drama",
            "scared": "Horror", "scary": "Horror",
            "excited": "Action", "thrilling": "Thriller",
            "romantic": "Romance", "love": "Romance",
            "thoughtful": "Sci-Fi", "mind-bending": "Sci-Fi"
        }

    def process_message(self, message, user_prefs):
        """Process a message and return a response."""
        msg_lower = message.lower().strip()

        # Greeting
        if any(g in msg_lower for g in ["hello", "hi ", "hey", "good morning", "good evening", "what's up", "yo", "howdy"]):
            if user_prefs.get("genres") or user_prefs.get("actors"):
                name = session.get("user_name", "")
                return f"Welcome back{f' {name}' if name else ''}! Ready to discover your next favorite movie? 🎬"
            return "Hey there! I'm Movie Buddy. Tell me what kind of movies you enjoy, and I'll find the perfect pick for you! 🍿"

        # Thanks
        if any(t in msg_lower for t in ["thanks", "thank you", "appreciate it"]):
            return "You're welcome! Happy watching! 🎬"

        # Bye
        if any(b in msg_lower for b in ["bye", "goodbye", "see you", "later"]):
            return "Goodbye! Come back anytime for more recommendations! 🍿"

        # Recommend
        if any(phrase in msg_lower for phrase in ["recommend", "suggest", "what should i watch", "what to watch", "give me", "show me"]):
            return self._generate_recommendation(user_prefs)

        # Mood-based
        for mood, genre in self.mood_map.items():
            if mood in msg_lower:
                return f"Since you're feeling {mood}, I'd suggest some {genre.lower()} movies! Use the browse section to find top {genre.lower()} films."

        # Extract genre preferences
        for keyword, genre in self.genre_keywords.items():
            if keyword in msg_lower:
                if any(word in msg_lower for word in ["hate", "don't like", "dislike", "not a fan", "avoid"]):
                    return f"Got it! I'll avoid {genre.lower()} movies in your recommendations."
                else:
                    return f"Nice! I'll remember you enjoy {genre.lower()} movies. You can also tell me your favorite actors or directors!"

        # Show what I know
        if any(phrase in msg_lower for phrase in ["what do you know", "what do you remember", "my taste", "my preferences", "about me", "remember me"]):
            prefs_summary = []
            if user_prefs.get("genres"):
                prefs_summary.append(f"genres: {', '.join(user_prefs['genres'])}")
            if user_prefs.get("actors"):
                prefs_summary.append(f"actors: {', '.join(user_prefs['actors'])}")
            if user_prefs.get("directors"):
                prefs_summary.append(f"directors: {', '.join(user_prefs['directors'])}")
            if prefs_summary:
                return f"Here's what I know about you! {'. '.join(prefs_summary)}."
            return "I don't know much about your taste yet! Tell me what genres, actors, or directors you enjoy."

        # Search request
        if any(phrase in msg_lower for phrase in ["search for", "find", "looking for", "look for"]):
            search_term = message
            for phrase in ["search for", "find", "looking for", "look for"]:
                search_term = search_term.replace(phrase, "").strip()
            if search_term:
                movies = tmdb.search_movies(search_term)
                if movies:
                    titles = [m["title"] for m in movies[:5]]
                    return f"I found some movies matching '{search_term}': {', '.join(titles)}. Check them out in the search section!"
                else:
                    return f"Sorry, I couldn't find any movies matching '{search_term}'."

        # Help
        if any(h in msg_lower for h in ["help", "what can you do", "commands"]):
            return ("I can help you find movies! Here's what I do:\n"
                    "🎯 Recommend movies based on your taste\n"
                    "🔍 Search for any movie\n"
                    "😊 Suggest movies based on your mood\n"
                    "💾 Remember your preferences\n"
                    "❤️ Save favorites and rate movies\n"
                    "Just tell me what you're into!")

        # Default - try to extract any movie-related intent
        if user_prefs.get("genres") or user_prefs.get("actors"):
            return "Interesting! I'm always learning. Try asking for recommendations, or tell me more about what you're looking for!"
        return "I'd love to help you find movies! Tell me what genres you enjoy - like Action, Comedy, Sci-Fi, or Horror - and I'll learn your taste!"

    def _generate_recommendation(self, user_prefs):
        """Generate a recommendation response."""
        genres = user_prefs.get("genres", [])
        actors = user_prefs.get("actors", [])
        directors = user_prefs.get("directors", [])

        if not genres and not actors and not directors:
            return "I don't know your taste yet! Tell me what kind of movies you like, and I'll find the perfect recommendation for you."

        reason_parts = []
        if genres:
            reason_parts.append(f"you enjoy {', '.join(genres).lower()}")
        if actors:
            reason_parts.append(f"you like {', '.join(actors)}")
        if directors:
            reason_parts.append(f"you're a fan of {', '.join(directors)}")

        reason = " and ".join(reason_parts)

        # Get recommendations
        recommended = []
        if genres:
            recommended = tmdb.get_by_genre(genres)
        if not recommended:
            recommended = tmdb.get_top_rated(1)

        if recommended:
            top_titles = [m["title"] for m in recommended[:3]]
            return f"Based on {reason}, I think you'll love: {', '.join(top_titles)}! Check out the recommendations section for more! 🎬"

        return f"Based on {reason}, I'd suggest browsing our popular movies section!"


chatbot = MovieChatBot()


@app.route("/api/chat", methods=["POST"])
def chat():
    """Process a chat message."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    message = data["message"].strip()
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Save user message
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, role, content) VALUES (?, ?, ?)",
                   (user_id, "user", message))

    # Get user preferences
    cursor.execute("SELECT pref_type, pref_value FROM preferences WHERE user_id = ?", (user_id,))
    prefs_rows = cursor.fetchall()
    user_prefs = {"genres": [], "actors": [], "directors": [], "disliked_genres": []}
    for row in prefs_rows:
        ptype = row["pref_type"]
        pval = row["pref_value"]
        if ptype in user_prefs:
            user_prefs[ptype].append(pval)

    # Process message and extract preferences
    msg_lower = message.lower()

    # Extract genre preferences from message
    for keyword, genre in chatbot.genre_keywords.items():
        if keyword in msg_lower:
            if any(word in msg_lower for word in ["hate", "don't like", "dislike", "not a fan", "avoid"]):
                cursor.execute("""
                    INSERT OR IGNORE INTO preferences (user_id, pref_type, pref_value)
                    VALUES (?, 'disliked_genres', ?)
                """, (user_id, genre))
            else:
                cursor.execute("""
                    INSERT OR IGNORE INTO preferences (user_id, pref_type, pref_value)
                    VALUES (?, 'genres', ?)
                """, (user_id, genre))

    # Extract actor preferences
    actor_keywords = {
        "keanu": "Keanu Reeves", "reeves": "Keanu Reeves",
        "leonardo": "Leonardo DiCaprio", "dicaprio": "Leonardo DiCaprio",
        "brad pitt": "Brad Pitt", "tom hanks": "Tom Hanks",
        "ryan gosling": "Ryan Gosling", "gosling": "Ryan Gosling",
        "ryan reynolds": "Ryan Reynolds", "reynolds": "Ryan Reynolds",
        "christian bale": "Christian Bale", "bale": "Christian Bale",
        "robert downey": "Robert Downey Jr.", "morgan freeman": "Morgan Freeman",
        "scarlett": "Scarlett Johansson", "johansson": "Scarlett Johansson",
        "diCaprio": "Leonardo DiCaprio"
    }
    for keyword, actor in actor_keywords.items():
        if keyword in msg_lower:
            cursor.execute("""
                INSERT OR IGNORE INTO preferences (user_id, pref_type, pref_value)
                VALUES (?, 'actors', ?)
            """, (user_id, actor))

    # Extract director preferences
    director_keywords = {
        "nolan": "Christopher Nolan", "christopher nolan": "Christopher Nolan",
        "tarantino": "Quentin Tarantino", "quentin": "Quentin Tarantino",
        "scorsese": "Martin Scorsese", "martin scorsese": "Martin Scorsese",
        "cameron": "James Cameron", "james cameron": "James Cameron",
        "fincher": "David Fincher", "david fincher": "David Fincher",
        "spielberg": "Steven Spielberg", "steven spielberg": "Steven Spielberg"
    }
    for keyword, director in director_keywords.items():
        if keyword in msg_lower:
            cursor.execute("""
                INSERT OR IGNORE INTO preferences (user_id, pref_type, pref_value)
                VALUES (?, 'directors', ?)
            """, (user_id, director))

    db.commit()

    # Try AI response first, fall back to rule-based chatbot
    if ai_chat.is_available():
        # Build movie context for AI
        movie_context = ""
        if user_prefs.get("genres"):
            movie_context = f"Preferred genres: {', '.join(user_prefs['genres'])}"
        
        ai_response = ai_chat.generate_response(message, user_prefs, movie_context)
        if ai_response:
            response = ai_response
        else:
            response = chatbot.process_message(message, user_prefs)
    else:
        response = chatbot.process_message(message, user_prefs)

    # Save bot response
    cursor.execute("INSERT INTO chat_history (user_id, role, content) VALUES (?, ?, ?)",
                   (user_id, "assistant", response))
    db.commit()

    return jsonify({"response": response, "success": True})


@app.route("/api/chat/history", methods=["GET"])
def get_chat_history():
    """Get chat history for current user."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT role, content, timestamp FROM chat_history
        WHERE user_id = ? ORDER BY timestamp ASC
    """, (user_id,))

    messages = [{"role": row["role"], "content": row["content"], "timestamp": row["timestamp"]}
                for row in cursor.fetchall()]
    return jsonify({"messages": messages})


# ============================================================
# PERSONALIZED RECOMMENDATIONS
# ============================================================

@app.route("/api/recommendations/personalized", methods=["GET"])
def get_personalized_recommendations():
    """Get personalized movie recommendations based on user preferences."""
    user_id = session.get("user_id")
    if not user_id:
        # Return popular movies for unauthenticated users
        movies = tmdb.get_popular()
        return jsonify({"movies": movies, "reason": "Popular Movies"})

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT pref_type, pref_value FROM preferences WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()

    genres = []
    actors = []
    directors = []
    disliked_genres = []

    for row in rows:
        if row["pref_type"] == "genres":
            genres.append(row["pref_value"])
        elif row["pref_type"] == "actors":
            actors.append(row["pref_value"])
        elif row["pref_type"] == "directors":
            directors.append(row["pref_value"])
        elif row["pref_type"] == "disliked_genres":
            disliked_genres.append(row["pref_value"])

    # Get watched movies
    cursor.execute("SELECT movie_title FROM watch_history WHERE user_id = ?", (user_id,))
    watched = [row["movie_title"] for row in cursor.fetchall()]

    # Get favorites
    cursor.execute("SELECT movie_title FROM favorites WHERE user_id = ?", (user_id,))
    favorites = [row["movie_title"] for row in cursor.fetchall()]

    if not genres and not actors and not directors:
        movies = tmdb.get_top_rated()
        return jsonify({"movies": movies, "reason": "Top Rated Movies"})

    reason_parts = []
    if genres:
        reason_parts.append(f"You like {', '.join(genres)}")

    # Get movies by preferred genres
    recommended = tmdb.get_by_genre(genres) if genres else tmdb.get_popular()

    # Filter out watched and favorited movies from recommendations
    filtered = [m for m in recommended if m["title"] not in watched and m["title"] not in favorites]

    if not filtered:
        filtered = tmdb.get_top_rated()

    if genres:
        reason_parts.append(f"You like {', '.join(genres)}")
    else:
        reason_parts.append("Your preferences")

    return jsonify({
        "movies": filtered[:10],
        "reason": " and ".join(reason_parts)
    })


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    init_db()
    print("🎬 MovieBuddy Web API Server")
    print(f"📁 Database: {DATABASE_PATH}")
    print("🌐 http://localhost:5001")
    app.run(debug=True, port=5001)
