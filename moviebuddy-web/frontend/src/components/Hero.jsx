import React, { useState, useEffect } from 'react';
import('./Hero.css');

function Hero({ movies, onMovieClick, onPlay }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);

  const currentMovie = movies[currentIndex];

  useEffect(() => {
    if (!movies || movies.length === 0) return;
    const interval = setInterval(() => {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentIndex(prev => (prev + 1) % Math.min(movies.length, 5));
        setIsTransitioning(false);
      }, 300);
    }, 8000);
    return () => clearInterval(interval);
  }, [movies]);

  if (!movies || movies.length === 0) {
    return (
      <div className="hero hero-placeholder">
        <div className="hero-content">
          <h1 className="hero-title">Welcome to MovieBuddy</h1>
          <p className="hero-description">
            Your personal AI movie recommendation assistant. Discover new films, 
            build your watchlist, and get personalized suggestions.
          </p>
        </div>
        <div className="hero-gradient" />
      </div>
    );
  }

  return (
    <div className="hero" style={{ backgroundImage: currentMovie?.backdrop ? `url(${currentMovie.backdrop})` : 'none' }}>
      <div className="hero-overlay" />
      <div className={`hero-content ${isTransitioning ? 'fade-out' : 'fade-in'}`}>
        {currentMovie && (
          <>
            <div className="hero-badge">Featured</div>
            <h1 className="hero-title">{currentMovie.title}</h1>
            <div className="hero-meta">
              {currentMovie.year && <span className="hero-year">{currentMovie.year}</span>}
              {currentMovie.rating && (
                <span className="hero-rating">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="#ffd700" stroke="#ffd700" strokeWidth="1">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                  </svg>
                  {currentMovie.rating}/10
                </span>
              )}
              {currentMovie.genre && <span className="hero-genre">{currentMovie.genre}</span>}
            </div>
            <p className="hero-description">{currentMovie.overview}</p>
            <div className="hero-actions">
              <button
                className="hero-btn hero-btn-primary"
                onClick={() => {
                  onPlay(currentMovie.title, currentMovie.id);
                  onMovieClick(currentMovie);
                }}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="5 3 19 12 5 21 5 3" />
                </svg>
                Play
              </button>
              <button
                className="hero-btn hero-btn-secondary"
                onClick={() => onMovieClick(currentMovie)}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="16" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12.01" y2="8" />
                </svg>
                More Info
              </button>
            </div>
          </>
        )}
      </div>
      <div className="hero-indicators">
        {movies.slice(0, 5).map((_, i) => (
          <button
            key={i}
            className={`hero-dot ${i === currentIndex ? 'active' : ''}`}
            onClick={() => {
              setIsTransitioning(true);
              setTimeout(() => {
                setCurrentIndex(i);
                setIsTransitioning(false);
              }, 300);
            }}
          />
        ))}
      </div>
      <div className="hero-gradient" />
    </div>
  );
}

export default Hero;