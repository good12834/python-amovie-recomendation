import React, { useState, useRef, useEffect } from 'react';
import { Search, Clapperboard } from 'lucide-react';
import { api } from '../api/api';
import './SearchBar.css';

function SearchBar({ onMovieClick, onClose }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const inputRef = useRef(null);
  const searchTimeout = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSearch = async (searchQuery) => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    setIsSearching(true);
    try {
      const data = await api.searchMovies(searchQuery);
      setResults(data.movies || []);
    } catch {
      setResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);

    if (searchTimeout.current) {
      clearTimeout(searchTimeout.current);
    }

    searchTimeout.current = setTimeout(() => {
      handleSearch(value);
    }, 400);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  return (
    <div className="search-overlay" onClick={onClose}>
      <div className="search-modal" onClick={e => e.stopPropagation()}>
        <div className="search-input-container">
          <svg className="search-input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          <input
            ref={inputRef}
            type="text"
            className="search-input"
            placeholder="Search for movies, actors, genres..."
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
          {query && (
            <button className="search-clear" onClick={() => {
              setQuery('');
              setResults([]);
              inputRef.current?.focus();
            }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          )}
        </div>

        <div className="search-results">
          {isSearching && (
            <div className="search-loading">
              <div className="search-spinner" />
              <span>Searching...</span>
            </div>
          )}

          {!isSearching && results.length === 0 && query && (
            <div className="search-empty">
              <span className="search-empty-icon"><Search size={32} /></span>
              <p className="search-empty-text">No movies found for "{query}"</p>
            </div>
          )}

          {!isSearching && results.length === 0 && !query && (
            <div className="search-hints">
              <p className="search-hints-title">Popular searches</p>
              <div className="search-hints-tags">
                {['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror', 'Inception', 'The Dark Knight', 'Interstellar'].map(hint => (
                  <button
                    key={hint}
                    className="search-hint-tag"
                    onClick={() => {
                      setQuery(hint);
                      handleSearch(hint);
                    }}
                  >
                    {hint}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="search-results-grid">
            {results.map((movie) => (
              <div
                key={movie.id}
                className="search-result-item"
                onClick={() => {
                  onMovieClick(movie);
                  onClose();
                }}
              >
                <div className="search-result-poster">
                  {movie.poster || movie.poster_path ? (
                    <img
                      src={movie.poster || `https://image.tmdb.org/t/p/w92${movie.poster_path}`}
                      alt={movie.title}
                    />
                  ) : (
                    <div className="search-result-placeholder"><Clapperboard size={24} /></div>
                  )}
                </div>
                <div className="search-result-info">
                  <h4 className="search-result-title">{movie.title}</h4>
                  <div className="search-result-meta">
                    {movie.year && <span>{movie.year}</span>}
                    {(movie.rating || movie.vote_average) && (
                      <span className="search-result-rating">
                        ★ {movie.rating || movie.vote_average?.toFixed(1)}
                      </span>
                    )}
                  </div>
                  {movie.overview && (
                    <p className="search-result-overview">{movie.overview.slice(0, 100)}...</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default SearchBar;