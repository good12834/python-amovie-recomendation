import React, { useRef, useState } from 'react';
import MovieCard from './MovieCard';
import './MovieRow.css';

function MovieRow({ title, movies, onMovieClick, onFavorite, onRate, onPlay, user }) {
  const rowRef = useRef(null);
  const [scrollPosition, setScrollPosition] = useState(0);
  const [showLeftArrow, setShowLeftArrow] = useState(false);
  const [showRightArrow, setShowRightArrow] = useState(true);

  if (!movies || movies.length === 0) return null;

  const handleScroll = () => {
    if (rowRef.current) {
      const { scrollLeft, scrollWidth, clientWidth } = rowRef.current;
      setScrollPosition(scrollLeft);
      setShowLeftArrow(scrollLeft > 10);
      setShowRightArrow(scrollLeft < scrollWidth - clientWidth - 10);
    }
  };

  const scroll = (direction) => {
    if (rowRef.current) {
      const scrollAmount = direction === 'left' ? -400 : 400;
      rowRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  return (
    <div className="movie-row">
      <h2 className="movie-row-title">{title}</h2>
      <div className="movie-row-container">
        {showLeftArrow && (
          <button className="row-arrow row-arrow-left" onClick={() => scroll('left')}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15 18 9 12 15 6" />
            </svg>
          </button>
        )}
        <div
          className="movie-row-track"
          ref={rowRef}
          onScroll={handleScroll}
        >
          {movies.map((movie, index) => (
            <MovieCard
              key={movie.id || index}
              movie={movie}
              onMovieClick={onMovieClick}
              onFavorite={onFavorite}
              onRate={onRate}
              onPlay={onPlay}
              user={user}
            />
          ))}
        </div>
        {showRightArrow && (
          <button className="row-arrow row-arrow-right" onClick={() => scroll('right')}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}

export default MovieRow;