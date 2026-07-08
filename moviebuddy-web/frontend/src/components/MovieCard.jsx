import React, { useState } from 'react';
import { Clapperboard } from 'lucide-react';
import './MovieCard.css';

function MovieCard({ movie, onMovieClick, onFavorite, onRate, onPlay, user }) {
  const [isHovered, setIsHovered] = useState(false);
  const [showRating, setShowRating] = useState(false);
  const [isFavorited, setIsFavorited] = useState(false);
  const [touchActive, setTouchActive] = useState(false);

  const handleFavorite = (e) => {
    e.stopPropagation();
    setIsFavorited(!isFavorited);
    onFavorite(movie);
  };

  const handleRate = (e, rating) => {
    e.stopPropagation();
    onRate(movie.title, rating);
    setShowRating(false);
  };

  const handleTouch = () => {
    setTouchActive(true);
    setTimeout(() => setTouchActive(false), 2000);
  };

  const posterUrl = movie.poster || null;

  return (
    <div
      className="movie-card"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => {
        setIsHovered(false);
        setShowRating(false);
      }}
      onTouchStart={handleTouch}
      onClick={() => onMovieClick(movie)}
    >
      <div className="movie-card-poster">
        {posterUrl ? (
          <img src={posterUrl} alt={movie.title} loading="lazy" />
        ) : (
          <div className="movie-card-placeholder">
            <span className="movie-placeholder-icon"><Clapperboard size={32} /></span>
            <span className="movie-placeholder-title">{movie.title}</span>
          </div>
        )}
        <div className={`movie-card-overlay ${(isHovered || touchActive) ? 'visible' : ''}`}>
          <button
            className="movie-card-btn movie-card-play"
            onClick={(e) => {
              e.stopPropagation();
              if (onPlay) {
                onPlay(movie);
              }
            }}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="5 3 19 12 5 21 5 3" />
            </svg>
          </button>
          <div className="movie-card-actions">
            <button
              className={`movie-card-btn ${isFavorited ? 'favorited' : ''}`}
              onClick={handleFavorite}
              title={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill={isFavorited ? '#e50914' : 'none'} stroke="currentColor" strokeWidth="2">
                <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
              </svg>
            </button>
            <button
              className="movie-card-btn"
              onClick={(e) => {
                e.stopPropagation();
                setShowRating(!showRating);
              }}
              title="Rate movie"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
              </svg>
            </button>
          </div>
          {showRating && (
            <div className="movie-card-rating" onClick={e => e.stopPropagation()}>
              {[1, 2, 3, 4, 5].map(r => (
                <button
                  key={r}
                  className="rating-star"
                  onClick={(e) => handleRate(e, r * 2)}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ffd700" strokeWidth="2">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                  </svg>
                </button>
              ))}
            </div>
          )}
        </div>
        <div className="movie-card-rating-badge">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="#ffd700">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
          </svg>
          {movie.rating || movie.vote_average?.toFixed(1) || 'N/A'}
        </div>
      </div>
      <div className="movie-card-info">
        <h4 className="movie-card-title">{movie.title}</h4>
        <div className="movie-card-meta">
          {movie.year && <span>{movie.year}</span>}
          {movie.genre && <span className="movie-card-genre">{movie.genre}</span>}
        </div>
      </div>
    </div>
  );
}

export default MovieCard;