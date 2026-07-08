import React, { useState, useEffect } from 'react';
import { api } from '../api/api';
import './TrailerPlayer.css';

function TrailerPlayer({ movie, onClose }) {
  const [video, setVideo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    async function fetchVideo() {
      try {
        const data = await api.getMovieVideos(movie.id);
        if (!cancelled) {
          if (data.videos && data.videos.length > 0) {
            setVideo(data.videos[0]);
          } else {
            setError('No trailer available for this movie.');
          }
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError('Failed to load trailer.');
          setLoading(false);
        }
      }
    }
    fetchVideo();
    return () => { cancelled = true; };
  }, [movie.id]);

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="trailer-overlay" onClick={handleOverlayClick}>
      <div className="trailer-modal">
        <button className="trailer-close" onClick={onClose}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        <div className="trailer-header">
          <span className="trailer-badge">Trailer</span>
          <h2 className="trailer-title">{movie.title}</h2>
        </div>

        <div className="trailer-content">
          {loading && (
            <div className="trailer-loading">
              <div className="loading-spinner"></div>
              <p>Loading trailer...</p>
            </div>
          )}

          {error && (
            <div className="trailer-error">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              <p>{error}</p>
              <p className="trailer-error-hint">You can still view movie details.</p>
            </div>
          )}

          {video && (
            <div className="trailer-video-wrapper">
              <iframe
                className="trailer-video"
                src={`https://www.youtube.com/embed/${video.key}?autoplay=1&rel=0`}
                title={`${movie.title} Trailer`}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TrailerPlayer;