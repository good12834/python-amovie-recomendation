import React, { useState } from 'react';
import './MovieDetail.css';

function MovieDetail({ movie, onClose, onFavorite, onRate, onPlay, user }) {
  const [rating, setRating] = useState(0);
  const [showRatingPicker, setShowRatingPicker] = useState(false);

  const backdropUrl = movie.backdrop || null;
  const posterUrl = movie.poster || null;

  const handleRate = (value) => {
    setRating(value);
    onRate(movie.title, value * 2);
    setShowRatingPicker(false);
  };

  return (
    <div className="detail-overlay" onClick={onClose}>
      <div className="detail-modal" onClick={e => e.stopPropagation()}>
        <button className="detail-close" onClick={onClose}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        <div className="detail-backdrop" style={{ backgroundImage: backdropUrl ? `url(${backdropUrl})` : 'none' }}>
          <div className="detail-backdrop-overlay" />
          <div className="detail-backdrop-content">
            {posterUrl && (
              <img src={posterUrl} alt={movie.title} className="detail-poster" />
            )}
            <div className="detail-hero-info">
              <h1 className="detail-title">{movie.title}</h1>
              <div className="detail-meta">
                {movie.year && <span className="detail-year">{movie.year}</span>}
                {movie.runtime && <span className="detail-runtime">{movie.runtime} min</span>}
                {(movie.rating || movie.vote_average) && (
                  <span className="detail-rating">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="#ffd700" stroke="#ffd700" strokeWidth="1">
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                    </svg>
                    {movie.rating || movie.vote_average?.toFixed(1)}/10
                  </span>
                )}
                {movie.vote_count && (
                  <span className="detail-votes">({movie.vote_count.toLocaleString()} votes)</span>
                )}
              </div>
              {movie.genre && (
                <div className="detail-genres">
                  {movie.genre.split(',').map((g, i) => (
                    <span key={i} className="detail-genre-tag">{g.trim()}</span>
                  ))}
                </div>
              )}
              <div className="detail-actions">
                <button
                  className="detail-btn detail-btn-primary"
                  onClick={() => onPlay(movie.title, movie.id)}
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3" />
                  </svg>
                  Play
                </button>
                <button
                  className="detail-btn detail-btn-secondary"
                  onClick={() => onFavorite(movie)}
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
                  </svg>
                  Favorite
                </button>
                <button
                  className="detail-btn detail-btn-secondary"
                  onClick={() => setShowRatingPicker(!showRatingPicker)}
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                  </svg>
                  Rate
                </button>
              </div>
              {showRatingPicker && (
                <div className="detail-rating-picker">
                  <span className="rating-picker-label">Rate this movie:</span>
                  <div className="rating-stars">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        className={`rating-star-btn ${rating >= star ? 'active' : ''}`}
                        onClick={() => handleRate(star)}
                      >
                        <svg width="28" height="28" viewBox="0 0 24 24" fill={rating >= star ? '#ffd700' : 'none'} stroke="#ffd700" strokeWidth="2">
                          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                        </svg>
                      </button>
                    ))}
                  </div>
                  <span className="rating-value">{rating * 2}/10</span>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="detail-body">
          {movie.tagline && (
            <p className="detail-tagline">{movie.tagline}</p>
          )}
          <div className="detail-section">
            <h3 className="detail-section-title">Overview</h3>
            <p className="detail-overview">{movie.overview}</p>
          </div>

          {movie.director && (
            <div className="detail-section">
              <h3 className="detail-section-title">Director</h3>
              <p className="detail-person">{movie.director}</p>
            </div>
          )}

          {movie.actors && movie.actors.length > 0 && (
            <div className="detail-section">
              <h3 className="detail-section-title">Cast</h3>
              <div className="detail-cast">
                {movie.actors.map((actor, i) => (
                  <span key={i} className="cast-member">{actor}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MovieDetail;