import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p"

# Fallback movie data if TMDB API key is not set
FALLBACK_MOVIES = [
    {"id": 1, "title": "The Shawshank Redemption", "genre": "Drama", "rating": 9.3, "year": 1994, "director": "Frank Darabont", "actors": ["Tim Robbins", "Morgan Freeman"], "poster": "", "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."},
    {"id": 2, "title": "The Godfather", "genre": "Crime", "rating": 9.2, "year": 1972, "director": "Francis Ford Coppola", "actors": ["Marlon Brando", "Al Pacino", "James Caan"], "poster": "", "overview": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son."},
    {"id": 3, "title": "The Dark Knight", "genre": "Action", "rating": 9.0, "year": 2008, "director": "Christopher Nolan", "actors": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"], "poster": "", "overview": "When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest tests."},
    {"id": 4, "title": "Pulp Fiction", "genre": "Crime", "rating": 8.9, "year": 1994, "director": "Quentin Tarantino", "actors": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"], "poster": "", "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption."},
    {"id": 5, "title": "Forrest Gump", "genre": "Drama", "rating": 8.8, "year": 1994, "director": "Robert Zemeckis", "actors": ["Tom Hanks", "Robin Wright", "Gary Sinise"], "poster": "", "overview": "The presidencies of Kennedy and Johnson through the eyes of an Alabama man with an IQ of 75."},
    {"id": 6, "title": "Inception", "genre": "Sci-Fi", "rating": 8.8, "year": 2010, "director": "Christopher Nolan", "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"], "poster": "", "overview": "A thief who steals corporate secrets through dream-sharing technology is given the task of planting an idea."},
    {"id": 7, "title": "The Matrix", "genre": "Sci-Fi", "rating": 8.7, "year": 1999, "director": "Lana Wachowski", "actors": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"], "poster": "", "overview": "A computer hacker learns about the true nature of reality and his role in the war against its controllers."},
    {"id": 8, "title": "Interstellar", "genre": "Sci-Fi", "rating": 8.7, "year": 2014, "director": "Christopher Nolan", "actors": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"], "poster": "", "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."},
    {"id": 9, "title": "Parasite", "genre": "Thriller", "rating": 8.5, "year": 2019, "director": "Bong Joon-ho", "actors": ["Kang-ho Song", "Sun-kyun Lee", "Yeo-jeong Jo"], "poster": "", "overview": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan."},
    {"id": 10, "title": "Spirited Away", "genre": "Animation", "rating": 8.6, "year": 2001, "director": "Hayao Miyazaki", "actors": ["Rumi Hiiragi", "Miyu Irino", "Mari Natsuki"], "poster": "", "overview": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches and spirits."},
    {"id": 11, "title": "The Avengers", "genre": "Action", "rating": 8.0, "year": 2012, "director": "Joss Whedon", "actors": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson"], "poster": "", "overview": "Earth's mightiest heroes must come together to stop the mischievous Loki from enslaving humanity."},
    {"id": 12, "title": "Joker", "genre": "Drama", "rating": 8.4, "year": 2019, "director": "Todd Phillips", "actors": ["Joaquin Phoenix", "Robert De Niro", "Zazie Beetz"], "poster": "", "overview": "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society."},
    {"id": 13, "title": "La La Land", "genre": "Romance", "rating": 8.3, "year": 2016, "director": "Damien Chazelle", "actors": ["Ryan Gosling", "Emma Stone", "John Legend"], "poster": "", "overview": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations."},
    {"id": 14, "title": "Get Out", "genre": "Horror", "rating": 7.7, "year": 2017, "director": "Jordan Peele", "actors": ["Daniel Kaluuya", "Allison Williams", "Bradley Whitford"], "poster": "", "overview": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception eventually reaches a boiling point."},
    {"id": 15, "title": "Mad Max: Fury Road", "genre": "Action", "rating": 8.1, "year": 2015, "director": "George Miller", "actors": ["Tom Hardy", "Charlize Theron", "Nicholas Hoult"], "poster": "", "overview": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners."},
    {"id": 16, "title": "The Silence of the Lambs", "genre": "Thriller", "rating": 8.6, "year": 1991, "director": "Jonathan Demme", "actors": ["Jodie Foster", "Anthony Hopkins", "Lawrence A. Bonney"], "poster": "", "overview": "A young FBI cadet must receive the help of an incarcerated and manipulative cannibal killer to catch another serial killer."},
    {"id": 17, "title": "Coco", "genre": "Animation", "rating": 8.4, "year": 2017, "director": "Lee Unkrich", "actors": ["Anthony Gonzalez", "Gael García Bernal", "Benjamin Bratt"], "poster": "", "overview": "Aspiring musician Miguel, confronted with his family's ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather."},
    {"id": 18, "title": "Whiplash", "genre": "Drama", "rating": 8.5, "year": 2014, "director": "Damien Chazelle", "actors": ["Miles Teller", "J.K. Simmons", "Melissa Benoist"], "poster": "", "overview": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing."},
    {"id": 19, "title": "Avengers: Endgame", "genre": "Action", "rating": 8.4, "year": 2019, "director": "Anthony Russo", "actors": ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo"], "poster": "", "overview": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more."},
    {"id": 20, "title": "The Truman Show", "genre": "Comedy", "rating": 8.2, "year": 1998, "director": "Peter Weir", "actors": ["Jim Carrey", "Laura Linney", "Ed Harris"], "poster": "", "overview": "An insurance salesman discovers his whole life is actually a reality TV show."}
]


class TMDBAPI:
    """Wrapper for The Movie Database (TMDB) API."""

    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.access_token = TMDB_ACCESS_TOKEN
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}" if self.access_token else ""
        })
        self.use_fallback = (not self.api_key or self.api_key == "your_tmdb_api_key_here") and not self.access_token

    def _get(self, endpoint, params=None):
        """Make a GET request to TMDB API."""
        if self.use_fallback:
            return None
        try:
            url = f"{TMDB_BASE_URL}/{endpoint}"
            if params is None:
                params = {}
            params["api_key"] = self.api_key
            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            return None

    def search_movies(self, query, page=1):
        """Search for movies by title."""
        if self.use_fallback:
            return self._fallback_search(query)

        data = self._get("search/movie", {"query": query, "page": page, "language": "en-US"})
        if data and "results" in data:
            return self._format_results(data["results"])
        return self._fallback_search(query)

    def get_popular(self, page=1):
        """Get popular movies."""
        if self.use_fallback:
            return self._fallback_get_all()

        data = self._get("movie/popular", {"page": page, "language": "en-US"})
        if data and "results" in data:
            return self._format_results(data["results"])
        return self._fallback_get_all()

    def get_top_rated(self, page=1):
        """Get top rated movies."""
        if self.use_fallback:
            sorted_fb = sorted(FALLBACK_MOVIES, key=lambda x: x.get("rating", 0), reverse=True)
            return sorted_fb[:10]

        data = self._get("movie/top_rated", {"page": page, "language": "en-US"})
        if data and "results" in data:
            return self._format_results(data["results"])
        return self._fallback_get_top()

    def get_movie_details(self, movie_id):
        """Get details for a specific movie."""
        if self.use_fallback:
            for m in FALLBACK_MOVIES:
                if m["id"] == movie_id:
                    return m
            return FALLBACK_MOVIES[0]

        data = self._get(f"movie/{movie_id}", {"language": "en-US", "append_to_response": "credits"})
        if data:
            return self._format_single(data)
        return None

    def get_movie_videos(self, movie_id):
        """Get videos (trailers) for a specific movie."""
        if self.use_fallback:
            return []
        data = self._get(f"movie/{movie_id}/videos", {"language": "en-US"})
        if data and "results" in data:
            trailers = [v for v in data["results"] if v.get("type") == "Trailer" and v.get("site") == "YouTube"]
            if not trailers:
                trailers = [v for v in data["results"] if v.get("site") == "YouTube"]
            return trailers[:1]  # Return first trailer
        return []

    def get_recommendations(self, movie_id):
        """Get recommendations based on a movie."""
        if self.use_fallback:
            import random
            return random.sample(FALLBACK_MOVIES, min(5, len(FALLBACK_MOVIES)))

        data = self._get(f"movie/{movie_id}/recommendations", {"language": "en-US"})
        if data and "results" in data:
            return self._format_results(data["results"][:10])
        return []

    def get_by_genre(self, genres, page=1):
        """Discover movies by genre."""
        if self.use_fallback:
            results = [m for m in FALLBACK_MOVIES if m["genre"] in genres]
            return results[:10]

        genre_ids = self._get_genre_ids(genres)
        if not genre_ids:
            return self._fallback_search_by_genre(genres)

        data = self._get("discover/movie", {
            "with_genres": ",".join(str(g) for g in genre_ids),
            "page": page,
            "language": "en-US",
            "sort_by": "vote_average.desc",
            "vote_count.gte": 50
        })
        if data and "results" in data:
            return self._format_results(data["results"])
        return []

    def _get_genre_ids(self):
        """Get TMDB genre ID mapping."""
        data = self._get("genre/movie/list", {"language": "en-US"})
        if data and "genres" in data:
            return {g["name"]: g["id"] for g in data["genres"]}
        return {}

    def _get_genre_ids(self, genre_names):
        """Get TMDB genre IDs from names."""
        all_genres = self._get("genre/movie/list", {"language": "en-US"})
        if not all_genres or "genres" not in all_genres:
            return None

        genre_map = {g["name"].lower(): g["id"] for g in all_genres["genres"]}
        ids = []
        for name in genre_names:
            if name.lower() in genre_map:
                ids.append(genre_map[name.lower()])
        return ids if ids else None

    def _format_results(self, results):
        """Format TMDB API results into our standard format."""
        formatted = []
        for movie in results[:20]:
            poster_path = movie.get("poster_path") or movie.get("poster_path")
            backdrop_path = movie.get("backdrop_path") or movie.get("backdrop_path")
            formatted.append({
                "id": movie.get("id"),
                "title": movie.get("title", "Unknown"),
                "genre_ids": movie.get("genre_ids", []),
                "genre": "",
                "rating": round(movie.get("vote_average", 0), 1),
                "year": movie.get("release_date", "")[:4] if movie.get("release_date") else None,
                "poster": f"{TMDB_IMAGE_BASE}/w500{poster_path}" if poster_path else "",
                "backdrop": f"{TMDB_IMAGE_BASE}/w1280{backdrop_path}" if backdrop_path else "",
                "overview": movie.get("overview", ""),
                "vote_count": movie.get("vote_count", 0)
            })
        return formatted

    def _format_single(self, movie):
        """Format a single movie detail response."""
        poster_path = movie.get("poster_path")
        backdrop_path = movie.get("backdrop_path")
        return {
            "id": movie.get("id"),
            "title": movie.get("title", "Unknown"),
            "genre": ", ".join([g["name"] for g in movie.get("genres", [])]),
            "rating": round(movie.get("vote_average", 0), 1),
            "year": movie.get("release_date", "")[:4] if movie.get("release_date") else None,
            "poster": f"{TMDB_IMAGE_BASE}/w500{poster_path}" if poster_path else "",
            "backdrop": f"{TMDB_IMAGE_BASE}/w1280{backdrop_path}" if backdrop_path else "",
            "overview": movie.get("overview", ""),
            "runtime": movie.get("runtime"),
            "tagline": movie.get("tagline", ""),
            "vote_count": movie.get("vote_count", 0),
            "director": next((c["name"] for c in movie.get("credits", {}).get("crew", []) if c["job"] == "Director"), ""),
            "actors": [c["name"] for c in movie.get("credits", {}).get("cast", [])[:5]]
        }

    def _fallback_search(self, query):
        """Fallback search using local movie database."""
        query = query.lower()
        results = []
        for movie in FALLBACK_MOVIES:
            if (query in movie["title"].lower() or
                query in movie["genre"].lower() or
                query in movie.get("director", "").lower() or
                any(query in actor.lower() for actor in movie.get("actors", []))):
                results.append(movie)
        return results

    def _fallback_search_by_genre(self, genres):
        """Fallback genre search using local movie database."""
        results = [m for m in FALLBACK_MOVIES if m["genre"] in genres]
        results.sort(key=lambda x: x.get("rating", 0), reverse=True)
        return results[:10]

    def _fallback_get_all(self):
        """Return all fallback movies."""
        return FALLBACK_MOVIES

    def _fallback_get_top(self):
        """Return top fallback movies."""
        sorted_fb = sorted(FALLBACK_MOVIES, key=lambda x: x.get("rating", 0), reverse=True)
        return sorted_fb[:10]

    def get_genres_list(self):
        """Get list of all available genres."""
        if self.use_fallback:
            genres = sorted(set(m["genre"] for m in FALLBACK_MOVIES))
            return [{"id": i+1, "name": g} for i, g in enumerate(genres)]

        data = self._get("genre/movie/list", {"language": "en-US"})
        if data and "genres" in data:
            return data["genres"]
        genres = sorted(set(m["genre"] for m in FALLBACK_MOVIES))
        return [{"id": i+1, "name": g} for i, g in enumerate(genres)]