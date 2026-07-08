import json
import os
from datetime import datetime


class Memory:
    """Manages user preferences and memory persistence."""

    def __init__(self, users_file="users.json", history_file="data/history.json",
                 ratings_file="data/ratings.json", favorites_file="data/favorites.json"):
        self.users_file = users_file
        self.history_file = history_file
        self.ratings_file = ratings_file
        self.favorites_file = favorites_file
        self.current_user = None
        self._users = self._load_json(self.users_file)
        self._history = self._load_json(self.history_file)
        self._ratings = self._load_json(self.ratings_file)
        self._favorites = self._load_json(self.favorites_file)

    def _load_json(self, filepath):
        """Load JSON data from a file."""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return {}

    def _save_json(self, filepath, data):
        """Save JSON data to a file."""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def login(self, username):
        """Login as an existing user or create a new one."""
        if username not in self._users:
            self._users[username] = {
                "genres": [],
                "actors": [],
                "directors": [],
                "watched": [],
                "favorites": [],
                "disliked_genres": [],
                "disliked_movies": [],
                "country": "",
                "language": "",
                "age": ""
            }
            self._save_json(self.users_file, self._users)

        self.current_user = username
        return self._users[username]

    def get_user_memory(self):
        """Get the memory for the current user."""
        if not self.current_user:
            return {}
        return self._users.get(self.current_user, {})

    def update_memory(self, key, value):
        """Update a specific memory key for the current user."""
        if not self.current_user:
            return False

        memory = self._users[self.current_user]

        if key in ["genres", "actors", "directors", "disliked_genres"]:
            if value not in memory[key]:
                memory[key].append(value)
        elif key == "disliked_movies":
            if value not in memory[key]:
                memory[key].append(value)
        elif key in ["country", "language", "age"]:
            memory[key] = value

        self._save_json(self.users_file, self._users)
        return True

    def add_watched_movie(self, movie_title):
        """Add a movie to the user's watch history."""
        if not self.current_user:
            return False

        memory = self._users[self.current_user]
        if movie_title not in memory["watched"]:
            memory["watched"].append(movie_title)

        # Also add to history with date
        if self.current_user not in self._history:
            self._history[self.current_user] = []

        self._history[self.current_user].append({
            "movie": movie_title,
            "watched_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self._save_json(self.users_file, self._users)
        self._save_json(self.history_file, self._history)
        return True

    def add_favorite(self, movie_title):
        """Add a movie to the user's favorites."""
        if not self.current_user:
            return False

        memory = self._users[self.current_user]
        if movie_title not in memory["favorites"]:
            memory["favorites"].append(movie_title)

        if self.current_user not in self._favorites:
            self._favorites[self.current_user] = []

        if movie_title not in self._favorites[self.current_user]:
            self._favorites[self.current_user].append(movie_title)

        self._save_json(self.users_file, self._users)
        self._save_json(self.favorites_file, self._favorites)
        return True

    def rate_movie(self, movie_title, rating):
        """Rate a movie."""
        if not self.current_user:
            return False

        if self.current_user not in self._ratings:
            self._ratings[self.current_user] = {}

        # Update rating (keep highest if re-rating)
        if movie_title in self._ratings[self.current_user]:
            old = self._ratings[self.current_user][movie_title]
            self._ratings[self.current_user][movie_title] = max(old, rating)
        else:
            self._ratings[self.current_user][movie_title] = rating

        self._save_json(self.ratings_file, self._ratings)
        return True

    def get_ratings(self):
        """Get ratings for the current user."""
        if not self.current_user:
            return {}
        return self._ratings.get(self.current_user, {})

    def get_watch_history(self):
        """Get watch history for the current user."""
        if not self.current_user:
            return []
        return self._history.get(self.current_user, [])

    def get_favorites(self):
        """Get favorites for the current user."""
        if not self.current_user:
            return []
        memory = self._users.get(self.current_user, {})
        return memory.get("favorites", [])

    def clear_memory(self):
        """Clear all memory for the current user."""
        if not self.current_user:
            return False

        self._users[self.current_user] = {
            "genres": [],
            "actors": [],
            "directors": [],
            "watched": [],
            "favorites": [],
            "disliked_genres": [],
            "disliked_movies": [],
            "country": "",
            "language": "",
            "age": ""
        }

        if self.current_user in self._history:
            del self._history[self.current_user]
        if self.current_user in self._ratings:
            del self._ratings[self.current_user]
        if self.current_user in self._favorites:
            del self._favorites[self.current_user]

        self._save_json(self.users_file, self._users)
        self._save_json(self.history_file, self._history)
        self._save_json(self.ratings_file, self._ratings)
        self._save_json(self.favorites_file, self._favorites)
        return True

    def extract_preferences(self, text):
        """Extract preferences from natural language text."""
        text_lower = text.lower()
        updates = []

        # Genre preferences
        genre_keywords = {
            "action": "Action", "sci-fi": "Sci-Fi", "scifi": "Sci-Fi",
            "comedy": "Comedy", "drama": "Drama", "horror": "Horror",
            "thriller": "Thriller", "romance": "Romance", "crime": "Crime",
            "animation": "Animation", "anime": "Anime", "superhero": "Superhero",
            "marvel": "Superhero", "dc": "Superhero"
        }

        for keyword, genre in genre_keywords.items():
            if keyword in text_lower:
                # Check if it's a like or dislike
                if any(word in text_lower for word in ["hate", "don't like", "dislike", "not a fan", "avoid"]):
                    updates.append(("disliked_genres", genre))
                else:
                    updates.append(("genres", genre))

        # Actor detection
        actor_keywords = {
            "keanu": "Keanu Reeves", "reeves": "Keanu Reeves",
            "leonardo": "Leonardo DiCaprio", "dicaprio": "Leonardo DiCaprio",
            "brad pitt": "Brad Pitt", "tom hanks": "Tom Hanks",
            "ryan gosling": "Ryan Gosling", "gosling": "Ryan Gosling",
            "ryan reynolds": "Ryan Reynolds", "reynolds": "Ryan Reynolds",
            "christian bale": "Christian Bale", "bale": "Christian Bale",
            "robert downey": "Robert Downey Jr."
        }

        for keyword, actor in actor_keywords.items():
            if keyword in text_lower:
                updates.append(("actors", actor))

        # Director detection
        director_keywords = {
            "nolan": "Christopher Nolan", "christopher nolan": "Christopher Nolan",
            "tarantino": "Quentin Tarantino", "quentin": "Quentin Tarantino",
            "scorsese": "Martin Scorsese", "martin scorsese": "Martin Scorsese",
            "cameron": "James Cameron", "james cameron": "James Cameron",
            "fincher": "David Fincher", "david fincher": "David Fincher"
        }

        for keyword, director in director_keywords.items():
            if keyword in text_lower:
                updates.append(("directors", director))

        # Movie title detection
        movie_database = self._load_json("movies.json")
        for movie in movie_database:
            title_lower = movie["title"].lower()
            if title_lower in text_lower:
                # Check if it's "watched" context
                if any(word in text_lower for word in ["watched", "saw", "seen", "viewed"]):
                    updates.append(("watched", movie["title"]))
                # Check if it's favorite context
                if any(word in text_lower for word in ["amazing", "love", "great", "favorite", "awesome", "incredible", "fantastic", "best"]):
                    updates.append(("favorite", movie["title"]))

        return updates