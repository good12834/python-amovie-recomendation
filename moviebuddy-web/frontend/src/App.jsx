import React, { useState, useEffect, useCallback } from 'react';
import { Clapperboard, Target, Flame, Star, Theater, AlertTriangle } from 'lucide-react';
import { api } from './api/api';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import MovieRow from './components/MovieRow';
import ChatBot from './components/ChatBot';
import AuthModal from './components/AuthModal';
import MovieDetail from './components/MovieDetail';
import SearchBar from './components/SearchBar';
import TrailerPlayer from './components/TrailerPlayer';
import Footer from './components/Footer';
import './App.css';
import './components/Footer.css';

function App() {
  const [user, setUser] = useState(null);
  const [movies, setMovies] = useState({
    popular: [],
    topRated: [],
    trending: [],
    personalized: [],
  });
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState(null);
  const [genreMovies, setGenreMovies] = useState([]);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [trailerMovie, setTrailerMovie] = useState(null);
  const [showSearch, setShowSearch] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMovies = useCallback(async () => {
    try {
      const [popular, topRated, genresData] = await Promise.all([
        api.getPopular(),
        api.getTopRated(),
        api.getGenres(),
      ]);
      setMovies(prev => ({
        ...prev,
        popular: popular.movies,
        topRated: topRated.movies,
        trending: [...popular.movies].sort((a, b) => b.vote_count - a.vote_count).slice(0, 10),
      }));
      setGenres(genresData.genres || []);
    } catch (err) {
      setError(err.message);
    }
  }, []);

  const fetchPersonalized = useCallback(async () => {
    try {
      const data = await api.getPersonalized();
      setMovies(prev => ({
        ...prev,
        personalized: data.movies || [],
      }));
    } catch (err) {
      // Silent fail for personalized
    }
  }, []);

  const checkAuth = useCallback(async () => {
    try {
      const data = await api.getMe();
      if (data.user) {
        setUser(data.user);
        fetchPersonalized();
      }
    } catch {
      // User not logged in
    }
  }, [fetchPersonalized]);

  useEffect(() => {
    setLoading(true);
    Promise.all([fetchMovies(), checkAuth()])
      .finally(() => setLoading(false));
  }, [fetchMovies, checkAuth]);

  const handleLogin = async (name) => {
    try {
      const data = await api.login(name);
      if (data.success) {
        setUser(data.user);
        setShowAuthModal(false);
        fetchPersonalized();
      }
    } catch (err) {
      throw err;
    }
  };

  const handleLogout = async () => {
    try {
      await api.logout();
      setUser(null);
      setMovies(prev => ({ ...prev, personalized: [] }));
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  const handleGenreClick = async (genre) => {
    try {
      setSelectedGenre(genre);
      const data = await api.getMoviesByGenre(genre);
      setGenreMovies(data.movies || []);
    } catch (err) {
      console.error('Genre fetch error:', err);
    }
  };

  const handleMovieClick = async (movie) => {
    try {
      const data = await api.getMovieDetails(movie.id);
      setSelectedMovie(data.movie || movie);
    } catch {
      setSelectedMovie(movie);
    }
  };

  const handleAddFavorite = async (movie) => {
    if (!user) {
      setShowAuthModal(true);
      return;
    }
    try {
      await api.addFavorite({
        movie_title: movie.title,
        movie_id: movie.id,
        poster: movie.poster || '',
        year: movie.year,
        rating: movie.rating,
      });
    } catch (err) {
      console.error('Add favorite error:', err);
    }
  };

  const handleRateMovie = async (movieTitle, rating) => {
    if (!user) {
      setShowAuthModal(true);
      return;
    }
    try {
      await api.addRating(movieTitle, rating);
    } catch (err) {
      console.error('Rating error:', err);
    }
  };

  const handleWatchMovie = async (movieTitle, movieId) => {
    if (!user) {
      setShowAuthModal(true);
      return;
    }
    try {
      await api.addToWatchHistory(movieTitle, movieId);
    } catch (err) {
      console.error('Watch history error:', err);
    }
  };

  const handlePlayTrailer = async (movie) => {
    // Save to watch history if logged in
    if (user) {
      try {
        await api.addToWatchHistory(movie.title, movie.id);
      } catch (err) {
        console.error('Watch history error:', err);
      }
    }
    // Open trailer modal
    setTrailerMovie(movie);
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-content">
          <div className="loading-logo"><Clapperboard size={48} /></div>
          <div className="loading-spinner"></div>
          <p className="loading-text">Loading MovieBuddy...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <Navbar
        user={user}
        onLoginClick={() => setShowAuthModal(true)}
        onLogout={handleLogout}
        onChatClick={() => setShowChat(!showChat)}
        onSearchClick={() => setShowSearch(!showSearch)}
        showChat={showChat}
      />

      {showSearch && (
        <SearchBar
          onMovieClick={handleMovieClick}
          onClose={() => setShowSearch(false)}
        />
      )}

      <div className={`main-content ${showChat ? 'chat-open' : ''}`}>
        <Hero
          movies={movies.trending}
          onMovieClick={handleMovieClick}
          onPlay={handleWatchMovie}
        />

        <div className="browse-section">
          <div id="home"></div>
          {user && movies.personalized.length > 0 && (
            <div id="personalized">
              <MovieRow
                title={<><Target size={20} /> Recommended For You</>}
                movies={movies.personalized}
                onMovieClick={handleMovieClick}
                onFavorite={handleAddFavorite}
                onRate={handleRateMovie}
                onPlay={handlePlayTrailer}
                user={user}
              />
            </div>
          )}

          <div id="popular">
          <MovieRow
            title={<><Flame size={20} /> Popular Now</>}
            movies={movies.popular}
            onMovieClick={handleMovieClick}
            onFavorite={handleAddFavorite}
            onRate={handleRateMovie}
            onPlay={handlePlayTrailer}
            user={user}
          />
          </div>

          <div id="top-rated">
          <MovieRow
            title={<><Star size={20} /> Top Rated</>}
            movies={movies.topRated}
            onMovieClick={handleMovieClick}
            onFavorite={handleAddFavorite}
            onRate={handleRateMovie}
            onPlay={handlePlayTrailer}
            user={user}
          />
          </div>

          {genres.length > 0 && (
            <div className="genre-section" id="genres">
              <h2 className="section-title"><Theater size={20} /> Browse by Genre</h2>
              <div className="genre-grid">
                {genres.map((genre) => (
                  <button
                    key={genre.id}
                    className={`genre-chip ${selectedGenre === genre.name ? 'active' : ''}`}
                    onClick={() => handleGenreClick(genre.name)}
                  >
                    {genre.name}
                  </button>
                ))}
              </div>
              {selectedGenre && genreMovies.length > 0 && (
                <MovieRow
                  title={`${selectedGenre} Movies`}
                  movies={genreMovies}
                  onMovieClick={handleMovieClick}
                  onFavorite={handleAddFavorite}
                  onRate={handleRateMovie}
                  onPlay={handlePlayTrailer}
                  user={user}
                />
              )}
            </div>
          )}

          {error && (
            <div className="error-banner">
              <AlertTriangle size={16} /> {error}
            </div>
          )}
        </div>
      </div>

      <Footer 
        showChat={showChat} 
        onChatClick={() => setShowChat(!showChat)}
      />

      {showChat && (
        <ChatBot
          user={user}
          onLoginClick={() => setShowAuthModal(true)}
          onClose={() => setShowChat(false)}
          onMovieClick={handleMovieClick}
        />
      )}

      {showAuthModal && (
        <AuthModal
          onLogin={handleLogin}
          onClose={() => setShowAuthModal(false)}
        />
      )}

      {selectedMovie && (
        <MovieDetail
          movie={selectedMovie}
          onClose={() => setSelectedMovie(null)}
          onFavorite={handleAddFavorite}
          onRate={handleRateMovie}
          onPlay={(movieTitle, movieId) => handlePlayTrailer({ title: movieTitle, id: movieId })}
          user={user}
        />
      )}

      {trailerMovie && (
        <TrailerPlayer
          movie={trailerMovie}
          onClose={() => setTrailerMovie(null)}
        />
      )}
    </div>
  );
}

export default App;