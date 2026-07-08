import json
import os


class Recommender:
    """Movie recommendation engine."""

    def __init__(self, movies_file="movies.json"):
        self.movies_file = movies_file
        self._movies = self._load_movies()

    def _load_movies(self):
        """Load movie database from JSON."""
        try:
            if os.path.exists(self.movies_file):
                with open(self.movies_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return []

    def get_all_movies(self):
        """Get all movies in the database."""
        return self._movies

    def search_movies(self, query):
        """Search movies by title, genre, actor, or director."""
        query = query.lower()
        results = []

        for movie in self._movies:
            if (query in movie["title"].lower() or
                query in movie["genre"].lower() or
                query in movie.get("director", "").lower() or
                any(query in actor.lower() for actor in movie.get("actors", []))):
                results.append(movie)

        return results

    def recommend_by_genre(self, genres, watched=None, disliked_genres=None, limit=5):
        """Recommend movies based on preferred genres."""
        if watched is None:
            watched = []
        if disliked_genres is None:
            disliked_genres = []

        candidates = []
        for movie in self._movies:
            # Skip watched movies
            if movie["title"] in watched:
                continue
            # Skip disliked genres
            if movie["genre"] in disliked_genres:
                continue
            # Check if movie matches any preferred genre
            if movie["genre"] in genres:
                candidates.append(movie)

        # Sort by rating (descending) and return top N
        candidates.sort(key=lambda x: x.get("rating", 0), reverse=True)
        return candidates[:limit]

    def recommend_by_actor(self, actors, watched=None, disliked_genres=None, limit=5):
        """Recommend movies based on preferred actors."""
        if watched is None:
            watched = []
        if disliked_genres is None:
            disliked_genres = []

        candidates = []
        for movie in self._movies:
            if movie["title"] in watched:
                continue
            if movie["genre"] in disliked_genres:
                continue
            if any(actor in movie.get("actors", []) for actor in actors):
                candidates.append(movie)

        candidates.sort(key=lambda x: x.get("rating", 0), reverse=True)
        return candidates[:limit]

    def recommend_by_director(self, directors, watched=None, disliked_genres=None, limit=5):
        """Recommend movies based on preferred directors."""
        if watched is None:
            watched = []
        if disliked_genres is None:
            disliked_genres = []

        candidates = []
        for movie in self._movies:
            if movie["title"] in watched:
                continue
            if movie["genre"] in disliked_genres:
                continue
            if movie.get("director", "") in directors:
                candidates.append(movie)

        candidates.sort(key=lambda x: x.get("rating", 0), reverse=True)
        return candidates[:limit]

    def recommend_hybrid(self, memory, limit=5):
        """Recommend movies using all available preferences."""
        genres = memory.get("genres", [])
        actors = memory.get("actors", [])
        directors = memory.get("directors", [])
        watched = memory.get("watched", [])
        disliked_genres = memory.get("disliked_genres", [])

        if not genres and not actors and not directors:
            # No preferences yet, return top rated movies
            return self.get_top_rated(watched=watched, limit=limit)

        scored = {}
        for movie in self._movies:
            if movie["title"] in watched:
                continue
            if movie["genre"] in disliked_genres:
                continue

            score = 0.0

            # Genre match
            if movie["genre"] in genres:
                score += 3.0

            # Actor match
            if any(actor in movie.get("actors", []) for actor in actors):
                score += 2.0

            # Director match
            if movie.get("director", "") in directors:
                score += 2.0

            # Rating bonus (normalized)
            rating = movie.get("rating", 0)
            score += rating / 3.0  # Max ~3 points for a 9+ rated movie

            if score > 0:
                scored[movie["title"]] = {
                    "movie": movie,
                    "score": score
                }

        # Sort by score descending
        sorted_movies = sorted(scored.values(), key=lambda x: x["score"], reverse=True)
        return [item["movie"] for item in sorted_movies[:limit]]

    def get_top_rated(self, watched=None, limit=5):
        """Get top rated movies."""
        if watched is None:
            watched = []

        candidates = [m for m in self._movies if m["title"] not in watched]
        candidates.sort(key=lambda x: x.get("rating", 0), reverse=True)
        return candidates[:limit]

    def get_movie_by_title(self, title):
        """Get a movie by its exact title."""
        for movie in self._movies:
            if movie["title"].lower() == title.lower():
                return movie
        return None

    def get_movies_by_genre(self, genre):
        """Get all movies in a specific genre."""
        return [m for m in self._movies if m["genre"].lower() == genre.lower()]

    def get_genres(self):
        """Get all unique genres in the database."""
        genres = set()
        for movie in self._movies:
            genres.add(movie["genre"])
        return sorted(list(genres))